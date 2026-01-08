import logging
import socket
import requests
from jnius import autoclass, JavaException

# Android pyjnius classes
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
Context = autoclass('android.content.Context')
PackageManager = autoclass('android.content.pm.PackageManager')
Uri = autoclass('android.net.Uri')

ORBOT_PACKAGE = "org.torproject.android"
TORBROWSER_PACKAGE = "org.torproject.torbrowser"

# Known test .onion sites (safe, public)
ONION_TEST_URLS = [
    "http://3g2upl4pq6kufc4m.onion",  # DuckDuckGo onion
    "http://expyuzz4wqqyqhjn.onion",  # Facebook onion test
]

class TorRouting:
    """Real Orbot + Tor Browser + .onion Connectivity Test Thunder ∞ Pure"""
    def __init__(self, app):
        self.app = app
        self.activity = PythonActivity.mActivity
        self.context = self.activity.getPackageManager()

    def is_orbot_installed(self) -> bool:
        try:
            self.context.getPackageInfo(ORBOT_PACKAGE, PackageManager.GET_ACTIVITIES)
            return True
        except JavaException:
            return False

    def is_torbrowser_installed(self) -> bool:
        try:
            self.context.getPackageInfo(TORBROWSER_PACKAGE, PackageManager.GET_ACTIVITIES)
            return True
        except JavaException:
            return False

    def launch_orbot(self) -> bool:
        if not self.is_orbot_installed():
            return False
        try:
            intent = Intent("org.torproject.android.START_TOR")
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            self.activity.startActivity(intent)
            return True
        except Exception as e:
            logging.error(f"Orbot Launch Shadow: {e}")
            return False

    def launch_torbrowser(self, onion_url: str = "") -> bool:
        if not self.is_torbrowser_installed():
            return False
        try:
            intent = Intent(Intent.ACTION_VIEW)
            if onion_url:
                intent.setData(Uri.parse(onion_url))
            intent.setPackage(TORBROWSER_PACKAGE)
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            self.activity.startActivity(intent)
            return True
        except Exception as e:
            logging.error(f"Tor Browser Launch Shadow: {e}")
            return False

    def is_tor_proxy_active(self) -> bool:
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
        proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050',
        }
        try:
            response = requests.get("https://check.torproject.org/api/ip", proxies=proxies, timeout=15)
            return response.json().get("IsTor", False)
        except Exception as e:
            logging.warning(f"Tor Routing Test Shadow: {e}")
            return False

    def onion_connectivity_test(self) -> bool:
        proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050',
        }
        for url in ONION_TEST_URLS:
            try:
                response = requests.get(url, proxies=proxies, timeout=15)
                if response.status_code == 200:
                    logging.info(f".onion Connectivity Harmony: {url}")
                    return True
            except Exception as e:
                logging.warning(f".onion Test Shadow for {url}: {e}")
                continue
        return False

    def full_tor_verification(self) -> list[str]:
        anomalies = []

        if not self.is_orbot_installed() and not self.is_torbrowser_installed():
            anomalies.append("Tor App (Orbot/Tor Browser) Not Installed — Install Mercy")

        if not self.is_tor_proxy_active():
            anomalies.append("Tor Proxy Not Active — Launch Required")

        if not self.tor_routing_test():
            anomalies.append("Traffic Not Routed Through Tor — Shadow Critical")

        if not self.onion_connectivity_test():
            anomalies.append(".onion Connectivity Failed — Tor Routing Shadow")

        if not anomalies:
            logging.info("Tor Routing + .onion Connectivity Harmony Pure ∞")

        return anomalies
