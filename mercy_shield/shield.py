from jnius import autoclass, cast
from mercy_shield.sms_receiver import MercySMSReceiver
from mercy_shield.octonion_lite import oct_hash

Intent = autoclass('android.content.Intent')
Context = autoclass('android.content.Context')

class RealTimeShield:
    def __init__(self, lattice):
        self.lattice = lattice
        self.context = autoclass('org.kivy.android.PythonActivity').mActivity
        self.receiver = MercySMSReceiver(self)
        intent_filter = autoclass('android.content.IntentFilter')('android.provider.Telephony.SMS_RECEIVED')
        self.context.registerReceiver(self.receiver, intent_filter)
        print("MercyShield SMS receiver active — scam rhythm listening gentle")

    def handle_sms(self, sender: str, body: str):
        features = {
            "urgent_words": any(word in body.lower() for word in ["urgent", "immediate", "alert", "suspended", "warrant", "locked"]),
            "has_link": "http" in body.lower() or "www." in body or ".com" in body,
            "has_phone": any(c.isdigit() for c in body) and len([c for c in body if c.isdigit()]) > 5,
            "sender_unknown": not self.is_contact(sender),  # Stub contacts check
            "caps_ratio": sum(1 for c in body if c.isupper()) / len(body) if body else 0
        }
        threat_score = sum(features.values()) / len(features)  # Simple rhythm
        threat_hash = oct_hash((sender + body).encode())

        harmony = self.lattice.vote(threat_hash)
        if harmony < 0.7 or threat_score > 0.6:
            threat = {
                "type": "sms_scam",
                "desc": f"Scam SMS from {sender}: {body[:50]}...",
                "data": threat_hash
            }
            action = self.protect(threat)
            print(f"SMS threat: {action}")

    def is_contact(self, sender: str) -> bool:
        # Stub: real use ContactsContract query via pyjnius
        return False  # Conservative — unknown = shadow risk
