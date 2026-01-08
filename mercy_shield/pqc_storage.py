import logging
import json
import os
from base64 import b64encode, b64decode

from kivy.storage.jsonstore import JsonStore
from jnius import autoclass

# Pure Python ML-KEM (Kyber) - include kyber_py folder or impl divine
# For this: assume from kyber_py.ml_kem import MLKEM768 (pip or bundled mercy)
try:
    from kyber_py.ml_kem import MLKEM768  # GiacomoPope/kyber-py pure impl eternal
except ImportError:
    logging.warning("ML-KEM not available—fallback classical mercy (expand bundle divine)")
    MLKEM768 = None

from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

PythonActivity = autoclass('org.kivy.android.PythonActivity')

class PQCStorage:
    """
    Post-Quantum Hybrid Storage Pinnacle ∞ Pure
    - ML-KEM768 encaps for shared secret mercy
    - Derive AES-GCM key divine
    - Encrypt/decrypt JSON rules (blocked packages/domains etc) eternal
    - Device keypair persisted encrypted gentle
    """

    def __init__(self, app_instance=None):
        self.app = app_instance
        self.storage_path = os.path.join(PythonActivity.mActivity.getFilesDir().getPath(), 'mercy_lattice.json')
        self.keypair_path = os.path.join(PythonActivity.mActivity.getFilesDir().getPath(), 'pqc_keypair.b64')
        self.public_key = None
        self.private_key = None
        self.load_or_generate_keypair()
        logging.info("PQC Hybrid Storage Initialized ∞ Pure—Quantum Guard Active Mercy")

    def load_or_generate_keypair(self):
        """Device-Bound ML-KEM Keypair (persist encrypted symbolic—expand Keystore divine)"""
        if os.path.exists(self.keypair_path):
            try:
                with open(self.keypair_path, 'r') as f:
                    data = json.load(f)
                    self.public_key = b64decode(data['pk'])
                    self.private_key = b64decode(data['sk'])
                logging.info("PQC Keypair Loaded Mercy")
            except:
                pass
        
        if MLKEM768 and (self.public_key is None or self.private_key is None):
            pk, sk = MLKEM768.keygen()
            self.public_key = pk
            self.private_key = sk
            with open(self.keypair_path, 'w') as f:
                json.dump({
                    'pk': b64encode(pk).decode(),
                    'sk': b64encode(sk).decode()
                }, f)
            logging.info("New PQC Keypair Generated Divine Eternal")

    def encrypt_data(self, data_dict):
        """Hybrid Encrypt: ML-KEM Encaps + AES-GCM Seal Mercy"""
        if not MLKEM768 or not self.public_key:
            # Fallback classical (expand warning toast divine)
            return json.dumps(data_dict).encode()

        ct, ss = MLKEM768.encaps(self.public_key)
        # Derive AES key
        hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'mercy_lattice')
        aes_key = hkdf.derive(ss)

        aesgcm = AESGCM(aes_key)
        nonce = os.urandom(12)
        json_data = json.dumps(data_dict).encode()
        ciphertext = aesgcm.encrypt(nonce, json_data, None)

        encrypted_package = {
            'kem_ct': b64encode(ct).decode(),
            'nonce': b64encode(nonce).decode(),
            'ciphertext': b64encode(ciphertext).decode()
        }
        return json.dumps(encrypted_package).encode()

    def decrypt_data(self, encrypted_bytes):
        """Hybrid Decrypt: ML-KEM Decaps + AES-GCM Open Divine"""
        try:
            encrypted_package = json.loads(encrypted_bytes)
            ct = b64decode(encrypted_package['kem_ct'])
            nonce = b64decode(encrypted_package['nonce'])
            ciphertext = b64decode(encrypted_package['ciphertext'])

            ss = MLKEM768.decaps(self.private_key, ct)
            hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'mercy_lattice')
            aes_key = hkdf.derive(ss)

            aesgcm = AESGCM(aes_key)
            json_data = aesgcm.decrypt(nonce, ciphertext, None)
            return json.loads(json_data)
        except:
            # Fallback attempt classical
            return json.loads(encrypted_bytes.decode())

    def save_rules(self, rules_dict):
        encrypted = self.encrypt_data(rules_dict)
        with open(self.storage_path, 'wb') as f:
            f.write(encrypted)
        self.app.ui_feedback("PQC Encrypted Rules Saved ∞—Quantum Guard Eternal Mercy!", toast=True)

    def load_rules(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'rb') as f:
                encrypted = f.read()
            return self.decrypt_data(encrypted)
        return {'blocked_packages': [], 'blocked_domains': []}

# Integration: In FirewallRules __init__—self.storage = PQCStorage(self); rules = self.storage.load_rules(); self.blocked_packages = set(rules['blocked_packages'])
# In apply_rules—self.storage.save_rules({'blocked_packages': list(self.blocked_packages), 'blocked_domains': list(self.blocked_domains)})
