from jnius import autoclass, cast
from mercy_shield.mercy_burst import mercy_burst_confirm
from mercy_shield.octonion_lite import oct_hash
from mercy_shield.sms_receiver import MercySMSReceiver
from mercy_shield.contact_check import MercyContactCheck

Intent = autoclass('android.content.Intent')
Context = autoclass('android.content.Context')
ClipboardManager = autoclass('android.content.ClipboardManager')
ClipData = autoclass('android.content.ClipData')
Uri = autoclass('android.net.Uri')

class RealTimeShield:
    def __init__(self, lattice):
        self.lattice = lattice
        self.context = autoclass('org.kivy.android.PythonActivity').mActivity
        self.clipboard = cast(ClipboardManager, self.context.getSystemService(Context.CLIPBOARD_SERVICE))
        self.contact_check = MercyContactCheck(self.context)
        self.start_hooks()

    def start_hooks(self):
        # SMS receiver
        self.receiver = MercySMSReceiver(self)
        intent_filter = autoclass('android.content.IntentFilter')('android.provider.Telephony.SMS_RECEIVED')
        self.context.registerReceiver(self.receiver, intent_filter)

        # Clipboard listener (periodic low-power poll or callback stub)
        import threading
        threading.Thread(target=self.clipboard_watch, daemon=True).start()

        # Network, app install, etc. future grace
        print("MercyShield hooks active — lattice listening gentle (SMS + clipboard)")

    def clipboard_watch(self):
        last_clip = ""
        while True:
            if self.clipboard.hasPrimaryClip():
                clip = self.clipboard.getPrimaryClip()
                if clip:
                    item = clip.getItemAt(0)
                    text = str(item.getText()) if item.getText() else str(item.getUri())
                    if text != last_clip and text:
                        last_clip = text
                        self.handle_clipboard(text)
            import time
            time.sleep(2)  # Low-power poll — future OnPrimaryClipChangedListener

    def handle_clipboard(self, text: str):
        features = {
            "shortener": any(short in text.lower() for short in ["bit.ly", "tinyurl", "t.co", "goo.gl"]),
            "mismatch": "login" in text.lower() and "bank" not in text.lower(),  # Stub rhythm
            "suspicious_tld": text.endswith((".xyz", ".top", ".club"))
        }
        threat_score = sum(features.values()) / len(features)
        threat_hash = oct_hash(text.encode())

        harmony = self.lattice.vote(threat_hash)
        if harmony < 0.7 or threat_score > 0.5:
            threat = {
                "type": "clipboard_phish",
                "desc": f"Phishing link clipped: {text[:50]}...",
                "data": threat_hash
            }
            action = self.protect(threat)
            print(f"Clipboard threat: {action} — clear option mercy")

    def handle_sms(self, sender: str, body: str):
        # Existing SMS logic with contact_check
        is_known = self.contact_check.lookup(sender)
        # ... integrate into features/threat

    def protect(self, threat: dict):
        harmony = self.lattice.vote(threat["data"])
        if harmony < 0.7:
            if mercy_burst_confirm(threat):
                return "Mercy override — allowed gentle"
            # Future: clear clipboard or block connection
            return "Blocked — mercy burst divine"
        return "Harmony pure — allowed"
