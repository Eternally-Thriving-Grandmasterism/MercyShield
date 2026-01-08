import logging
import socket
import requests
from jnius import autoclass, JavaException

# Android pyjnius classes
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
Context = autoclass('android.content.Context')
PackageManager = autoclass('android.content.pm.PackageManager')

I2P_PACKAGE = "net.i2p.android.router"  # I2P Android router package

class I2PRouting:
    """Real I2P Router Integration Thunder ∞ Pure — Launch, Proxy Check, Eepsite Test"""
    def __init__(self, app):
        self.app = app
        self.activity = PythonActivity.mActivity
        self.context = self.activity.getPackageManager()

    def is_i2p_installed(self) -> bool:
        """Check if I2P Android router installed"""
        try:
            self.context.getPackageInfo(I2P_PACKAGE, PackageManager.GET_ACTIVITIES)
            return True
        except JavaException:
            return False

    def launch_i2p(self) -> bool:
        """Launch I2P router app"""
        if not self.is_i2p_installed():
            return False
        try:
            intent = Intent(Intent.ACTION_MAIN)
            intent.setPackage(I2P_PACKAGE)
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            self.activity.startActivity(intent)
            logging.info("I2P Launch Intent Sent Harmony ∞")
            return True
        except Exception as e:
            logging.error(f"I2P Launch Shadow: {e}")
            return False

    def is_i2p_proxy_active(self) -> bool:
        """Check common I2P HTTP proxy ports (4444/4445)"""
        i2p_ports = [4444, 4445]
        for port in i2p_ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(3)
                s.connect(('127.0.0.1', port))
                s.close()
                return True
            except:
                continue
        return False

    def i2p_connectivity_test(self) -> bool:
        """Test eepsite connectivity through I2P proxy"""
        proxies = {
            'http': 'http://127.0.0.1:4444',
            'https': 'http://127.0.0.1:4444',
        }
        test_eepsites = [
            "http://stats.i2p",
            "http://i2p-projekt.i2p",
        ]
        for url in test_eepsites:
            try:
                response = requests.get(url, proxies=proxies, timeout=20)
                if response.status_code == 200:
                    logging.info(f"I2P Eepsite Connectivity Harmony: {url}")
                    return True
            except Exception as e:
                logging.warning(f"I2P Test Shadow for {url}: {e}")
                continue
        return False

    def full_i2p_verification(self) -> list[str]:
        anomalies = []

        if not self.is_i2p_installed():
            anomalies.append("I2P Router App Not Installed — Install from F-Droid Mercy")

        if not self.is_i2p_proxy_active():
            anomalies.append("I2P Proxy Not Active — Launch Required")

        if not self.i2p_connectivity_test():
            anomalies.append("I2P Eepsite Connectivity Failed — Routing Shadow Critical")

        if not anomalies:
            logging.info("I2P Routing Harmony Pure ∞")

        return anomalies
