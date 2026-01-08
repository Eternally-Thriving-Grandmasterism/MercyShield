import logging
import socket
import requests
from jnius import autoclass

# Optional for real connection test
try:
    Context = autoclass('android.content.Context')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
except Exception as e:
    logging.warning(f"Tor Pyjnius Shadow: {e}")
    PythonActivity = None

# Known Tor check endpoints
TOR_CHECK_URL = "https://check.torproject.org/api/ip"
ONION_TEST = "http://expyuzz4wqqyqhjn.onion"  # Known test onion (or use known good)

class TorRouting:
    """Real Tor Routing Verification Thunder ∞ Pure — Proxy active + connection test"""
    def __init__(self, app):
        self.app = app

    def is_tor_proxy_active(self) -> bool:
        """Check common Tor SOCKS ports (Orbot default 9050/9150)"""
        tor_ports = [9050, 9150, 9051]
        for port in tor_ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                s.connect(('127.0.0.1', port))
                s.close()
                logging.info(f"Tor Proxy Active on Port {port} Harmony")
                return True
            except:
                continue
        return False

    def tor_connection_test(self) -> bool:
        """Test connection through Tor proxy (check.torproject.org)"""
        proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050',
        }
        try:
            response = requests.get(TOR_CHECK_URL, proxies=proxies, timeout=10)
            data = response.json()
            if data.get("IsTor", False):
                logging.info("Tor Connection Test Harmony Pure ∞")
                return True
        except Exception as e:
            logging.warning(f"Tor Connection Test Shadow: {e}")
        return False

    def full_tor_verification(self) -> list[str]:
        anomalies = []

        if not self.is_tor_proxy_active():
            anomalies.append("Tor Proxy Not Active — Routing Shadow Critical")

        if not self.tor_connection_test():
            anomalies.append("Tor Connection Failed — Not Routed Through Tor")

        if not anomalies:
            logging.info("Tor Routing Verification Harmony Pure ∞")

        return anomalies
