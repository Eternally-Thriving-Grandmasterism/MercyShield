import json
import datetime
from mercy_shield.encrypted import encrypt, decrypt

class MercyLog:
    def __init__(self, path="/sdcard/mercy_log.json"):
        self.path = path
        self.logs = self.load()

    def load(self):
        try:
            with open(self.path, 'r') as f:
                encrypted = f.read()
                return json.loads(decrypt(encrypted))
        except:
            return []

    def record(self, action: str, threat: dict, reason: str):
        entry = {
            "time": datetime.datetime.now().isoformat(),
            "action": action,
            "threat": threat.get("desc", "unknown"),
            "reason": reason
        }
        self.logs.append(entry)
        with open(self.path, 'w') as f:
            f.write(encrypt(json.dumps(self.logs, indent=2)))
