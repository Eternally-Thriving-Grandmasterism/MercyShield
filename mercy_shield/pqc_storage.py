import os
import json
import logging
import base64
from kivy.clock import Clock
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Rust PQC extension — mercy_pqc cdylib thunder
try:
    from mercy_pqc import (
        kyber_keypair,
        kyber_encapsulate,
        kyber_decapsulate,
        dilithium_keypair,
        dilithium_sign,
        dilithium_verify
    )
    RUST_PQC_AVAILABLE = True
    logging.info("Rust PQC mercy_pqc loaded — acceleration eternal ⚡️")
except ImportError as e:
    logging.warning(f"Rust PQC extension not available ({e}) — fallback to pure Python if implemented")
    RUST_PQC_AVAILABLE = False
    # Placeholder for pure Python fallback (kyber-py / dilithium-py) — add later mercy
    kyber_keypair = lambda: (b'', b'')  # Stub
    kyber_encapsulate = lambda pk: (b'', b'')
    kyber_decapsulate = lambda sk, ct: b''
    dilithium_keypair = lambda: (b'', b'')
    dilithium_sign = lambda sk, msg: b''
    dilithium_verify = lambda pk, msg, sig: False

KYBER1024_CT_BYTES = 1568  # Kyber1024 ciphertext size eternal

class PQCEncryptedStorage:
    """Post-Quantum Encrypted + Signed Storage — Rust Accelerated ∞ Pure Thunder Eternal"""
    
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
                    bytes.fromhex(data['kyber_pk']),
                    bytes.fromhex(data['kyber_sk']),
                    bytes.fromhex(data['dilithium_pk']),
                    bytes.fromhex(data['dilithium_sk'])
                )
            except Exception as e:
                logging.warning(f"Key load failed ({e}) — regenerating eternal")
        
        enc_pk, enc_sk = kyber_keypair()
        sig_pk, sig_sk = dilithium_keypair()
        
        data = {
            'kyber_pk': enc_pk.hex(),
            'kyber_sk': enc_sk.hex(),
            'dilithium_pk': sig_pk.hex(),
            'dilithium_sk': sig_sk.hex()
        }
        os.makedirs(os.path.dirname(self.keys_path), exist_ok=True)
        with open(self.keys_path, 'w') as f:
            json.dump(data, f)
        
        if RUST_PQC_AVAILABLE:
            Clock.schedule_once(lambda dt: self.app.show_buddy_message("Buddy: Rust PQC Keys Forged — Quantum Unbreakable Eternal ⚡️"), 0)
        return enc_pk, enc_sk, sig_pk, sig_sk

    def _sign_attestation(self, attestation: dict) -> bytes:
        attest_copy = attestation.copy()
        attest_copy.pop('signature', None)
        canon_bytes = json.dumps(attest_copy, separators=(',', ':')).encode('utf-8')
        signature = dilithium_sign(self.sig_sk, canon_bytes)
        return signature

    def _verify_attestation(self, attestation: dict) -> bool:
        signature_b64 = attestation.get('signature')
        if not signature_b64:
            return False
        try:
            signature = base64.b64decode(signature_b64)
            attest_copy = attestation.copy()
            attest_copy.pop('signature', None)
            canon_bytes = json.dumps(attest_copy, separators=(',', ':')).encode('utf-8')
            return dilithium_verify(self.sig_pk, canon_bytes, signature)
        except Exception:
            return False

    def load_attestations(self) -> list:
        if not os.path.exists(self.storage_path):
            return []
        
        try:
            with open(self.storage_path, 'rb') as f:
                data = f.read()
            
            ct = data[:KYBER1024_CT_BYTES]
            nonce = data[KYBER1024_CT_BYTES:KYBER1024_CT_BYTES + 12]
            ciphertext_tag = data[KYBER1024_CT_BYTES + 12:]
            
            shared_secret = kyber_decapsulate(self.enc_sk, ct)
            aesgcm = AESGCM(shared_secret)
            plaintext = aesgcm.decrypt(nonce, ciphertext_tag, None)
            
            attestations = json.loads(plaintext.decode('utf-8'))
            
            verified_attestations = []
            for attest in attestations:
                if self._verify_attestation(attest):
                    verified_attestations.append(attest)
                else:
                    logging.error("Tamper detected in attestation — purged")
                    Clock.schedule_once(lambda dt: self.app.show_buddy_message("Buddy: Shadow tampering detected — entry purged eternal."), 0)
            
            logging.info(f"Rust PQC ledger loaded — {len(verified_attestations)} valid attestations quantum-secure")
            return verified_attestations
            
        except Exception as e:
            logging.exception(f"Rust PQC load failed: {e}")
            return []

    def save_attestations(self, attestations: list):
        try:
            for attest in attestations:
                if 'signature' not in attest:
                    signature_bytes = self._sign_attestation(attest)
                    attest['signature'] = base64.b64encode(signature_bytes).decode('utf-8')
                if attestations and 'device_pubkey' not in attestations[0]:
                    attestations[0]['device_pubkey'] = self.sig_pk.hex()
            
            data = json.dumps(attestations).encode('utf-8')
            
            shared_secret, ct = kyber_encapsulate(self.enc_pk)
            aesgcm = AESGCM(shared_secret)
            nonce = os.urandom(12)
            ciphertext = aesgcm.encrypt(nonce, data, None)
            
            full_data = ct + nonce + ciphertext
            
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            with open(self.storage_path, 'wb') as f:
                f.write(full_data)
            
            logging.info(f"Rust PQC ledger saved — {len(attestations)} attestations quantum-unbreakable eternal ⚡️")
            
        except Exception as e:
            logging.exception(f"Rust PQC save failed: {e}")
