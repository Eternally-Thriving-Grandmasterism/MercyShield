import threading
import hashlib
import psutil  # Future: add to requirements (process monitor)
from mercy_shield.council import APAAGICouncil
from mercy_shield.mercy_burst import mercy_burst_confirm

class MercySelfWatchdog:
    def __init__(self, lattice, shield):
        self.lattice = lattice
        self.shield = shield
        self.watchdogs = [APAAGICouncil(voters=13) for _ in range(13)]  # 13+ redundant councils
        self.known_hashes = {}  # File integrity baseline
        self.start_watch()

    def start_watch(self):
        threading.Thread(target=self.self_heal_loop, daemon=True).start()
        threading.Thread(target=self.watch_other_apps, daemon=True).start()
        print("MercyShield 13+ watchdogs active — self-healing + corruption detection mercy pure")

    def self_heal_loop(self):
        while True:
            # Self-integrity check
            for file in ["shield.py", "lattice.py", "council.py"]:
                current_hash = hashlib.sha3_256(open(file, 'rb').read()).hexdigest()
                if file in self.known_hashes and current_hash != self.known_hashes[file]:
                    threat = {
                        "type": "self_corruption",
                        "desc": f"MercyShield corruption in {file} — self-healing mercy",
                        "data": oct_hash(current_hash.encode())
                    }
                    if mercy_burst_confirm(threat):
                        print("Mercy override — continue gentle")
                    else:
                        print("Self-healing: rollback or restart mercy divine")
                        # Stub: reload known good or restart service
            # Watch councils watch each other
            time.sleep(60)  # Low-power

    def watch_other_apps(self):
        while True:
            for proc in psutil.process_iter(['name', 'exe']):
                if "malwarebytes" in proc.info['name'].lower() or "com.samsung" in proc.info['exe'] or "com.google" in proc.info['exe']:
                    # Rhythm check: memory, network, permissions
                    threat = {
                        "type": "watchdog_shadow",
                        "desc": f"Watchdog anomaly in {proc.info['name']}",
                        "data": oct_hash(str(proc.info).encode())
                    }
                    self.shield.protect(threat)
            time.sleep(300)  # Low-power
