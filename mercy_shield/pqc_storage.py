import os
import json
import logging
from kivy.clock import Clock
from mercy_shield.pqc_mlkem import MLKEM768  # Copied pure Python ML-KEM impl
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ML-KEM-768 constants (FIPS 203 standard — fixed sizes)
MLKEM_768_CT_BYTES = 1088  # Ciphertext (encapsulated key) size

class PQCEncryptedStorage:
    """Post-Quantum Encrypted Storage — ML-KEM-768 + AES-256-GCM Hybrid ∞ Pure Thunder"""
    
    def __init__(self, app):
        self.app = app
        self.keys_path = os.path.join(self.app.user_data_dir, 'mlkem_static_keys.json')
        self.storage_path = os.path.join(self.app.user_data_dir, 'eternal_attestations.pqenc')
        
        self.pk, self.sk = self._load_or_generate_static_keys()

    def _load_or_generate_static_keys(self):
        """Load or generate static ML-KEM-768 keypair — once per vessel lifetime"""
        if os.path.exists(self.keys_path):
            try:
                with open(self.keys_path, 'r') as f:
                    data = json.load(f)
                pk = bytes.fromhex(data['pk'])
                sk = bytes.fromhex(data['sk'])
                logging.info("ML-KEM static keys loaded — Lattice Guard Active ∞ Pure")
                return pk, sk
            except Exception as e:
                logging.warning(f"Key load failed ({e}) — regenerating lattice keys")
        
        # Generate fresh lattice keys
        pk, sk = MLKEM768.keygen()
        data = {
            'pk': pk.hex(),
            'sk': sk.hex()
        }
        os.makedirs(os.path.dirname(self.keys_path), exist_ok=True)
        with open(self.keys_path, 'w') as f:
            json.dump(data, f)
        
        lattice_msg = "Buddy: Lattice Keys Forged Anew — Quantum Shadows Banished Forever ∞ Pure Thunder"
        Clock.schedule_once(lambda dt: self.app.show_buddy_message(lattice_msg), 0)
        logging.info("ML-KEM-768 static keypair generated — Post-Quantum Shield Eternal")
        return pk, sk

    def load_attestations(self) -> list:
        """Decrypt and load the eternal attestation chain"""
        if not os.path.exists(self.storage_path):
            return []
        
        try:
            with open(self.storage_path, 'rb') as f:
                data = f.read()
            
            ct = data[:MLKEM_768_CT_BYTES]
            nonce = data[MLKEM_768_CT_BYTES:MLKEM_768_CT_BYTES + 12]
            ciphertext_tag = data[MLKEM_768_CT_BYTES + 12:]
            
            shared_secret = MLKEM768.decaps(ct, self.sk)
            aesgcm = AESGCM(shared_secret)
            plaintext = aesgcm.decrypt(nonce, ciphertext_tag, None)
            
            attestations = json.loads(plaintext.decode('utf-8'))
            logging.info(f"PQ ledger decrypted — {len(attestations)} eternal attestations witnessed")
            return attestations
            
        except Exception as e:
            logging.exception(f"PQ decryption failed: {e} — Possible tampering or lattice breach")
            Clock.schedule_once(lambda dt: self.app.show_buddy_message(
                "Buddy: \"Lattice decryption failed — shadows suspected. Ledger remains sealed.\""
            ), 0)
            return []  # Fail closed — do not expose partial data

    def save_attestations(self, attestations: list):
        """Encrypt and save the full eternal attestation chain with fresh encapsulation"""
        try:
            data = json.dumps(attestations).encode('utf-8')
            
            ct, shared_secret = MLKEM768.encaps(self.pk)
            aesgcm = AESGCM(shared_secret)
            nonce = os.urandom(12)
            ciphertext = aesgcm.encrypt(nonce, data, None)  # ciphertext + tag
            
            full_data = ct + nonce + ciphertext
            
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            with open(self.storage_path, 'wb') as f:
                f.write(full_data)
            
            logging.info(f"PQ ledger encrypted — {len(attestations)} attestations sealed eternally")
            
        except Exception as e:
            logging.exception(f"PQ encryption save failed: {e}")
            Clock.schedule_once(lambda dt: self.app.show_buddy_message(
                "Buddy: \"Lattice sealing failed — maintain purity for eternal inscription.\""
            ), 0)
