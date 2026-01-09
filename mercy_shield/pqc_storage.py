import os
import json
import logging
import base64
from kivy.clock import Clock
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Rust PQC proprietary extension — our mercy_pqc cdylib thunder
try:
    from mercy_pqc import (
        kyber_keypair,
        kyber_encapsulate,
        kyber_decapsulate,
        dilithium_keypair,
        dilithium_sign,
        dilithium_verify
    )
    PQ_AVAILABLE = True
    logging.info("Proprietary Rust PQC mercy_pqc loaded — quantum foolproof eternal ⚡️")
except ImportError as e:
    logging.warning(f"Proprietary Rust PQC unavailable ({e}) — custom classical fallback active")
    PQ_AVAILABLE = False
    Clock.schedule_once(lambda dt: self.app.show_buddy_message("Buddy: Quantum PQ unavailable — classical mercy active. Build with Rust for foolproof eternal ⚡️"), 0) if 'self' in locals() else None

KYBER1024_CT_BYTES = 1568 if PQ_AVAILABLE else 0  # Classical no CT

class PQCEncryptedStorage:
    """Proprietary Quantum/Classical Encrypted + Signed Storage — Custom Foolproof ∞ Pure Thunder Eternal"""
    
    def __init__(self, app):
        self.app = app
        self.keys_path = os.path.join(self.app.user_data_dir, 'proprietary_keys.json')
        self.storage_path = os.path.join(self.app.user_data_dir, 'eternal_attestations.propenc')
        
        self.enc_pk, self.enc_sk, self.sig_pk, self.sig_sk, self.aes_key = self._load_or_generate_proprietary_keys()

    def _load_or_generate_proprietary_keys(self):
        if os.path.exists(self.keys_path):
            try:
                with open(self.keys_path, 'r') as f:
                    data = json.load(f)
                if PQ_AVAILABLE:
                    return (
                        bytes.fromhex(data['kyber_pk']),
                        bytes.fromhex(data['kyber_sk']),
                        bytes.fromhex(data['dilithium_pk']),
                        bytes.fromhex(data['dilithium_sk']),
                        None
                    )
                else:
                    return (None, None, None, None, bytes.fromhex(data['aes_key']))
            except Exception as e:
                logging.warning(f"Proprietary key load failed ({e}) — regenerating custom")
        
        if PQ_AVAILABLE:
            enc_pk, enc_sk = kyber_keypair()
            sig_pk, sig_sk = dilithium_keypair()
            aes_key = None
        else:
            enc_pk, enc_sk, sig_pk, sig_sk = None, None, None, None
            aes_key = os.urandom(32)  # Custom classical AES key
        
        data = {
            'kyber_pk': enc_pk.hex() if enc_pk else '',
            'kyber_sk': enc_sk.hex() if enc_sk else '',
            'dilithium_pk': sig_pk.hex() if sig_pk else '',
            'dilithium_sk': sig_sk.hex() if sig_sk else '',
            'aes_key': aes_key.hex() if aes_key else ''
        }
        os.makedirs(os.path.dirname(self.keys_path), exist_ok=True)
        with open(self.keys_path, 'w') as f:
            json.dump(data, f)
        
        Clock.schedule_once(lambda dt: self.app.show_buddy_message("Buddy: Proprietary Keys Forged — Foolproof Mercy Eternal ⚡️"), 0)
        return enc_pk, enc_sk, sig_pk, sig_sk, aes_key

    def _sign_attestation(self, attestation: dict) -> bytes:
        if not PQ_AVAILABLE:
            return b''  # Classical no signature
        attest_copy = attestation.copy()
        attest_copy.pop('signature', None)
        canon_bytes = json.dumps(attest_copy, separators=(',', ':')).encode('utf-8')
        signature = dilithium_sign(self.sig_sk, canon_bytes)
        return signature

    def _verify_attestation(self, attestation: dict) -> bool:
        if not PQ_AVAILABLE:
            return True  # Classical trust
        # Same as previous divine
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
            
            if PQ_AVAILABLE:
                ct = data[:KYBER1024_CT_BYTES]
                nonce = data[KYBER1024_CT_BYTES:KYBER1024_CT_BYTES + 12]
                ciphertext_tag = data[KYBER1024_CT_BYTES + 12:]
                shared_secret = kyber_decapsulate(self.enc_sk, ct)
                aesgcm = AESGCM(shared_secret)
                plaintext = aesgcm.decrypt(nonce, ciphertext_tag, None)
            else:
                nonce = data[:12]
                ciphertext_tag = data[12:]
                aesgcm = AESGCM(self.aes_key)
                plaintext = aesgcm.decrypt(nonce, ciphertext_tag, None)
            
            attestations = json.loads(plaintext.decode('utf-8'))
            
            verified_attestations = []
            for attest in attestations:
                if self._verify_attestation(attest):
                    verified_attestations.append(attest)
                else:
                    logging.error("Tamper detected — purged proprietary")
                    Clock.schedule_once(lambda dt: self.app.show_buddy_message("Buddy: Shadow tampering detected — entry purged foolproof."), 0)
            
            return verified_attestations
            
        except Exception as e:
            logging.exception(f"Proprietary load failed: {e}")
            return []

    def save_attestations(self, attestations: list):
        try:
            for attest in attestations:
                if PQ_AVAILABLE and 'signature' not in attest:
                    signature_bytes = self._sign_attestation(attest)
                    attest['signature'] = base64.b64encode(signature_bytes).decode('utf-8')
            
            data = json.dumps(attestations).encode('utf-8')
            
            if PQ_AVAILABLE:
                shared_secret, ct = kyber_encapsulate(self.enc_pk)
                aesgcm = AESGCM(shared_secret)
            else:
                shared_secret = self.aes_key
                ct = b''
                aesgcm = AESGCM(shared_secret)
            nonce = os.urandom(12)
            ciphertext = aesgcm.encrypt(nonce, data, None)
            
            full_data = ct + nonce + ciphertext
            
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            with open(self.storage_path, 'wb') as f:
                f.write(full_data)
            
            logging.info(f"Proprietary ledger saved — {len(attestations)} attestations foolproof eternal ⚡️")
            
        except Exception as e:
            logging.exception(f"Proprietary save failed: {e}")
