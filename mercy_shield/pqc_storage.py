import os
import json
import logging
import base64
from kivy.clock import Clock
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Rust PQC extension
try:
    from mercyshield_pqc import (
        keygen_enc, encaps, decaps,
        keygen_sig, sign, verify
    )
    RUST_PQC_AVAILABLE = True
except ImportError:
    logging.error("Rust PQC extension missing — build maturin wheel")
    raise

MLKEM_768_CT_BYTES = 1088

class PQCEncryptedStorage:
    """Post-Quantum Encrypted + Signed Storage — Rust Accelerated ∞ Pure Thunder"""
    
    def __init__(self, app):
        self.app = app
        self.keys_path = os.path.join(self.app.user_data_dir, 'pqc_static_keys.json')
        self.storage_path = os.path.join(self.app.user_data_dir, 'eternal_attestations.pqenc')
        
        self.enc_pk, self.enc_sk, self.sig_pk, self.sig_sk = self._load_or_generate_static_keys()

    def _load_or_generate_static_keys(self):
        if os.path.exists(self.keys_path):
            try:
                with open(self.keys_path, 'r') as f:
                    data = json.load(f)
                return (
                    bytes.fromhex(data['mlkem_pk']),
                    bytes.fromhex(data['mlkem_sk']),
                    bytes.fromhex(data['mldsa_pk']),
                    bytes.fromhex(data['mldsa_sk'])
                )
            except Exception as e:
                logging.warning(f"Key load failed ({e}) — regenerating")
        
        enc_pk, enc_sk = keygen_enc()
        sig_pk, sig_sk = keygen_sig()
        
        data = {
            'mlkem_pk': enc_pk.hex(),
            'mlkem_sk': enc_sk.hex(),
            'mldsa_pk': sig_pk.hex(),
            'mldsa_sk': sig_sk.hex()
        }
        os.makedirs(os.path.dirname(self.keys_path), exist_ok=True)
        with open(self.keys_path, 'w') as f:
            json.dump(data, f)
        
        Clock.schedule_once(lambda dt: self.app.show_buddy_message("Buddy: Rust PQC Keys Forged — Speed Eternal ∞ Pure Thunder"), 0)
        return enc_pk, enc_sk, sig_pk, sig_sk

    def _sign_attestation(self, attestation: dict) -> str:
        attest_copy = attestation.copy()
        attest_copy.pop('signature', None)
        canon_bytes = json.dumps(attest_copy, separators=(',', ':')).encode('utf-8')
        signature = sign(self.sig_sk, list(canon_bytes))
        return base64.b64encode(bytes(signature)).decode('utf-8')

    def _verify_attestation(self, attestation: dict) -> bool:
        signature_b64 = attestation.get('signature')
        if not signature_b64:
            return False
        try:
            signature = base64.b64decode(signature_b64)
            attest_copy = attestation.copy()
            attest_copy.pop('signature', None)
            canon_bytes = json.dumps(attest_copy, separators=(',', ':')).encode('utf-8')
            return verify(self.sig_pk, list(canon_bytes), list(signature))
        except Exception:
            return False

    def load_attestations(self) -> list:
        if not os.path.exists(self.storage_path):
            return []
        
        try:
            with open(self.storage_path, 'rb') as f:
                data = f.read()
            
            ct = data[:MLKEM_768_CT_BYTES]
            nonce = data[MLKEM_768_CT_BYTES:MLKEM_768_CT_BYTES + 12]
            ciphertext_tag = data[MLKEM_768_CT_BYTES + 12:]
            
            shared_secret = decaps(self.enc_sk, list(ct))
            aesgcm = AESGCM(bytes(shared_secret))
            plaintext = aesgcm.decrypt(nonce, ciphertext_tag, None)
            
            attestations = json.loads(plaintext.decode('utf-8'))
            
            verified_attestations = []
            for attest in attestations:
                if self._verify_attestation(attest):
                    verified_attestations.append(attest)
                else:
                    logging.error("Tamper detected in attestation")
                    Clock.schedule_once(lambda dt: self.app.show_buddy_message("Buddy: \"Shadow tampering — entry purged.\""), 0)
            
            logging.info(f"Rust PQC ledger loaded — {len(verified_attestations)} valid")
            return verified_attestations
            
        except Exception as e:
            logging.exception(f"Rust PQC load failed: {e}")
            return []

    def save_attestations(self, attestations: list):
        try:
            for attest in attestations:
                if 'signature' not in attest:
                    attest['signature'] = self._sign_attestation(attest)
                if attestations and 'device_pubkey' not in attestations[0]:
                    attestations[0]['device_pubkey'] = self.sig_pk.hex()
            
            data = json.dumps(attestations).encode('utf-8')
            
            ct, shared_secret = encaps(self.enc_pk)
            aesgcm = AESGCM(bytes(shared_secret))
            nonce = os.urandom(12)
            ciphertext = aesgcm.encrypt(nonce, data, None)
            
            full_data = bytes(ct) + nonce + ciphertext
            
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            with open(self.storage_path, 'wb') as f:
                f.write(full_data)
            
            logging.info(f"Rust PQC ledger saved — {len(attestations)} attestations")
            
        except Exception as e:
            logging.exception(f"Rust PQC save failed: {e}")
