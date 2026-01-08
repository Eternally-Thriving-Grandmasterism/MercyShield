import logging
import socket
import requests
from jnius import autoclass, JavaException

# Android pyjnius classes
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
Context = autoclass('android.content.Context')
PackageManager = autoclass('android.content.pm.PackageManager')

ORBOT_PACKAGE = "org.torproject.android"
ORBOT_START_ACTION = "org.torproject.android.START_TOR"

class TorRouting:
    """Real Orbot App Integration Thunder ∞ Pure — Launch, Proxy Check, Routing Test"""
    def __init__(self, app):
        self.app = app
        self.activity = PythonActivity.mActivity
        self.context = self.activity.getPackageManager()

    def is_orbot_installed(self) -> bool:
        """Check if Orbot app installed"""
        try:
            self.context.getPackageInfo(ORBOT_PACKAGE, PackageManager.GET_ACTIVITIES)
            return True
        except JavaException:
            return False

    def launch_orbot(self) -> bool:
        """Launch Orbot app/start intent"""
        if not self.is_orbot_installed():
            logging.warning("Orbot Not Installed — Mercy Shadow")
            return False

        try:
            intent = Intent()
            intent.setAction(ORBOT_START_ACTION)
            intent.addCategory(Intent.CATEGORY_DEFAULT)
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            self.activity.startActivity(intent)
            logging.info("Orbot Launch Intent Sent Harmony ∞")
            return True
        except Exception as e:
            logging.error(f"Orbot Launch Shadow: {e}")
            return False

    def is_tor_proxy_active(self) -> bool:
        """Check common Orbot SOCKS ports"""
        tor_ports = [9050, 9150, 9051]
        for port in tor_ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(3)
                s.connect(('127.0.0.1', port))
                s.close()
                return True
            except:
                continue
        return False

    def tor_routing_test(self) -> bool:
        """Test routing through Orbot proxy to check.torproject.org"""
        proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050',
        }
        try:
            response = requests.get("https://check.torproject.org/api/ip", proxies=proxies, timeout=15)
            data = response.json()
            return data.get("IsTor", False)
        except Exception as e:
            logging.warning(f"Tor Routing Test Shadow: {e}")
            return False

    def full_tor_verification(self) -> list[str]:
        anomalies = []

        if not self.is_orbot_installed():
            anomalies.append("Orbot App Not Installed — Install from F-Droid/Play Mercy")

        if not self.is_tor_proxy_active():
            anomalies.append("Orbot Proxy Not Active — Launch Orbot Required")
            # Auto-launch grace optional
            # self.launch_orbot()

        if not self.tor_routing_test():
            anomalies.append("Traffic Not Routed Through Tor — Shadow Critical")

        if not anomalies:
            logging.info("Orbot Tor Routing Harmony Pure ∞")

        return anomalies
