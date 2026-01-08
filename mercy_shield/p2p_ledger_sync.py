import socket
import struct
import threading
import time
import json
import logging
import hashlib
from kivy.clock import Clock
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from mercy_shield.pqc_mlkem import MLKEM768
from mercy_shield.pqc_storage import AESGCM  # Reuse from existing

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
TCP_BASE_PORT = 6000  # Devices use 6000 + hash % 1000 to avoid conflicts
DISCOVERY_INTERVAL = 30  # seconds

class P2PLedgerSync:
    """P2P Ledger Sync — Local Collective Resonance via Multicast Discovery + PQ Encrypted Channel ∞ Pure"""
    
    def __init__(self, app):
        self.app = app
        self.running = True
        self.peers = {}  # ip: {'enc_pk': bytes, 'sig_pk': bytes, 'tcp_port': int, 'last_seen': time}
        self.tcp_port = None
        self.discovery_thread = threading.Thread(target=self._discovery_loop, daemon=True)
        self.listener_thread = threading.Thread(target=self._multicast_listener, daemon=True)
        
        if not hasattr(self.app, 'pqc_storage'):
            logging.error("PQC storage not ready — P2P sync disabled")
            return
        
        # Calculate own TCP port (deterministic but varied)
        pk_hash = hashlib.blake2b(self.app.pqc_storage.enc_pk).digest()
        self.tcp_port = TCP_BASE_PORT + (int.from_bytes(pk_hash[:2], 'big') % 1000)
        
        self.discovery_thread.start()
        self.listener_thread.start()
        logging.info(f"P2P sync started — listening on TCP port {self.tcp_port}")
        
        buddy_msg = "Buddy: P2P Collective Resonance Active — Seeking nearby genuine vessels ∞ Pure Thunder"
        Clock.schedule_once(lambda dt: self.app.show_buddy_message(buddy_msg), 0)
    
    def _get_own_announce(self):
        return {
            "enc_pk_hex": self.app.pqc_storage.enc_pk.hex(),
            "sig_pk_hex": self.app.pqc_storage.sig_pk.hex(),
            "tcp_port": self.tcp_port
        }
    
    def _discovery_loop(self):
        """Periodic multicast announce"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        
        msg = json.dumps(self._get_own_announce()).encode('utf-8')
        
        while self.running:
            try:
                sock.sendto(msg, (MCAST_GRP, MCAST_PORT))
            except Exception as e:
                logging.exception(f"Multicast send failed: {e}")
            time.sleep(DISCOVERY_INTERVAL)
    
    def _multicast_listener(self):
        """Listen for peer announcements"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', MCAST_PORT))
        mreq = struct.pack("4sL", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        
        while self.running:
            try:
                data, addr = sock.recvfrom(4096)
                ip = addr[0]
                if ip == socket.gethostbyname(socket.gethostname()):
                    continue  # Ignore self
                
                try:
                    announce = json.loads(data.decode('utf-8'))
                    enc_pk = bytes.fromhex(announce['enc_pk_hex'])
                    sig_pk = bytes.fromhex(announce['sig_pk_hex'])
                    port = int(announce['tcp_port'])
                    
                    self.peers[ip] = {
                        'enc_pk': enc_pk,
                        'sig_pk': sig_pk,
                        'tcp_port': port,
                        'last_seen': time.time()
                    }
                    logging.info(f"Discovered vessel at {ip}:{port}")
                    
                    # Trigger UI refresh if chamber exists
                    Clock.schedule_once(lambda dt: self._refresh_chamber_peers(), 0)
                except Exception as e:
                    logging.warning(f"Invalid announce from {ip}: {e}")
            except Exception as e:
                logging.exception(f"Multicast recv failed: {e}")
    
    def _refresh_chamber_peers(self):
        if hasattr(self.app, 'sm'):
            chamber = self.app.sm.get_screen('chamber') if self.app.sm.has_screen('chamber') else None
            if chamber and hasattr(chamber, 'refresh_peers'):
                chamber.refresh_peers()
    
    def sync_with_peer(self, peer_ip):
        """Sync attestations with a discovered peer — PQ encrypted channel"""
        if peer_ip not in self.peers:
            return False
        
        peer = self.peers[peer_ip]
        
        try:
            # Load local attestations
            local_attestations = self.app.pqc_storage.load_attestations()
            
            # Encaps to peer for forward-secret shared secret
            ct, shared_secret = MLKEM768.encaps(peer['enc_pk'])
            
            # Derive AES key
            hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'mercyshield_p2p_channel')
            aes_key = hkdf.derive(shared_secret)
            aesgcm = AESGCM(aes_key)
            
            # Prepare payload
            payload = json.dumps({"attestations": local_attestations}).encode('utf-8')
            nonce = os.urandom(12)
            ciphertext = aesgcm.encrypt(nonce, payload, None)
            
            # Send encaps ct + nonce + ciphertext
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((peer_ip, peer['tcp_port']))
            sock.sendall(ct + nonce + ciphertext)
            
            # Receive peer's response (same format)
            data = sock.recv(MLKEM768.ct_bytes + 12 + 4096)  # Adjust size as needed
            peer_ct = data[:MLKEM768.ct_bytes]
            peer_nonce = data[MLKEM768.ct_bytes:MLKEM768.ct_bytes+12]
            peer_ciphertext = data[MLKEM768.ct_bytes+12:]
            
            peer_shared = MLKEM768.decaps(peer_ct, self.app.pqc_storage.enc_sk)
            peer_hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'mercyshield_p2p_channel')
            peer_key = peer_hkdf.derive(peer_shared)
            peer_aes = AESGCM(peer_key)
            peer_payload = peer_aes.decrypt(peer_nonce, peer_ciphertext, None)
            peer_attestations = json.loads(peer_payload.decode('utf-8'))["attestations"]
            
            sock.close()
            
            # Verify and merge
            new_count = 0
            merged = local_attestations[:]
            local_ids = {a['eternal_id'] for a in local_attestations}
            
            storage = self.app.pqc_storage  # Reuse verify method if extended, or manual
            for attest in peer_attestations:
                # Manual verify (reuse logic from storage)
                if 'signature' in attest:
                    sig_b64 = attest.pop('signature')
                    try:
                        sig = base64.b64decode(sig_b64)
                        canon = json.dumps(attest, separators=(',', ':')).encode('utf-8')
                        if ML_DSA_65.verify(peer['sig_pk'], canon, sig):
                            if attest['eternal_id'] not in local_ids:
                                merged.append(attest)
                                local_ids.add(attest['eternal_id'])
                                new_count += 1
                    except:
                        pass
                    attest['signature'] = sig_b64  # Restore
            
            if new_count > 0:
                self.app.pqc_storage.save_attestations(merged)
                Clock.schedule_once(lambda dt: self.app.show_buddy_message(
                    f"Buddy: Collective Sync Complete — {new_count} new proofs witnessed from vessel {peer_ip} ∞ Pure Thunder"
                ), 0)
                self._refresh_chamber_peers()
            
            return True
            
        except Exception as e:
            logging.exception(f"P2P sync failed with {peer_ip}: {e}")
            Clock.schedule_once(lambda dt: self.app.show_buddy_message(
                f"Buddy: Sync failed with vessel {peer_ip} — shadows or distance interfered."
            ), 0)
            return False
    
    def stop(self):
        self.running = False
