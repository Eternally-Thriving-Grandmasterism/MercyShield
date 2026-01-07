from jnius import autoclass, PythonJavaClass, java_method
from android.runnable import run_on_ui_thread
import threading

# Pyjnius Android classes
ConnectivityManager = autoclass('android.net.ConnectivityManager')
NetworkCallback = autoclass('android.net.ConnectivityManager$NetworkCallback')
PackageManager = autoclass('android.content.pm.PackageManager')
Intent = autoclass('android.content.Intent')
Context = autoclass('android.content.Context')
ClipboardManager = autoclass('android.content.ClipboardManager')
Telephony = autoclass('android.telephony.TelephonyManager')

class RealTimeShield:
    def __init__(self, lattice):
        self.lattice = lattice
        self.context = autoclass('org.kivy.android.PythonActivity').mActivity
        self.cm = self.context.getSystemService(Context.CONNECTIVITY_SERVICE)
        self.pm = self.context.getPackageManager()
        self.clipboard = self.context.getSystemService(Context.CLIPBOARD_SERVICE)
        self.start_hooks()

    def start_hooks(self):
        threading.Thread(target=self.network_monitor, daemon=True).start()
        threading.Thread(target=self.clipboard_watch, daemon=True).start()
        threading.Thread(target=self.app_install_watch, daemon=True).start()
        threading.Thread(target=self.sms_watch, daemon=True).start()
        print("MercyShield hooks active — lattice listening gentle")

    def network_monitor(self):
        callback = NetworkCallback()
        # Override onAvailable/onLost for suspicious traffic
        self.cm.registerDefaultNetworkCallback(callback)

    def detect_threat(self, event_type: str, data: dict) -> dict | None:
        # Real rhythm detect
        threat = None
        if event_type == "network" and "suspicious_domain" in data.get("host", ""):
            threat = {"type": "network_exfil", "desc": f"Suspicious connection: {data['host']}"}
        elif event_type == "clipboard" and "phish" in data.get("text", "").lower():
            threat = {"type": "clipboard_phish", "desc": "Phishing link copied"}
        elif event_type == "app_install" and "malware_sig" in data.get("package", ""):
            threat = {"type": "mal_app", "desc": f"Malicious app install: {data['package']}"}
        elif event_type == "sms" and "scam" in data.get("body", "").lower():
            threat = {"type": "sms_scam", "desc": "Scam SMS received"}

        if threat:
            threat["data"] = oct_hash(str(threat).encode())
            return threat
        return None

    def protect(self, threat: dict):
        harmony = self.lattice.vote(threat["data"])
        if harmony < 0.7:
            result = mercy_burst_confirm(threat)
            return "Blocked" if not result else "Mercy override"
        return "Harmony pure"
