import logging
import socket
import time
from jnius import autoclass, JavaException

# Android pyjnius classes
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
Context = autoclass('android.content.Context')
PackageManager = autoclass('android.content.pm.PackageManager')

I2P_PACKAGE = "net.i2p.android.router"

SAM_HOST = "127.0.0.1"
SAM_PORT = 7656  # Default SAM bridge v3.1

class I2PRouting:
    """Real I2P Router + SAM API Integration Thunder ∞ Pure — Launch, SAM Hello/Session, Proxy Fallback"""
    def __init__(self, app):
        self.app = app
        self.activity = PythonActivity.mActivity
        self.context = self.activity.getPackageManager()

    def is_i2p_installed(self) -> bool:
        try:
            self.context.getPackageInfo(I2P_PACKAGE, PackageManager.GET_ACTIVITIES)
            return True
        except JavaException:
            return False

    def launch_i2p(self) -> bool:
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

    def sam_hello_test(self) -> bool:
        """SAM v3.1 HELLO test — connect + HELLO VERSION"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((SAM_HOST, SAM_PORT))
            s.send(b"HELLO VERSION MIN=3.1 MAX=3.1\n")
            response = s.recv(1024).decode()
            s.close()
            if "HELLO REPLY RESULT=OK" in response:
                logging.info("I2P SAM API Harmony Pure ∞")
                return True
        except Exception as e:
            logging.warning(f"SAM Hello Shadow: {e}")
        return False

    def is_i2p_proxy_active(self) -> bool:
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
                    return True
            except:
                continue
        return False

    def full_i2p_verification(self) -> list[str]:
        anomalies = []

        if not self.is_i2p_installed():
            anomalies.append("I2P Router App Not Installed — Install from F-Droid Mercy")

        if not self.sam_hello_test():
            anomalies.append("I2P SAM API Not Active — Advanced Control Shadow")

        if not self.is_i2p_proxy_active():
            anomalies.append("I2P HTTP Proxy Not Active — Launch Required")

        if not self.i2p_connectivity_test():
            anomalies.append("I2P Eepsite Connectivity Failed — Routing Shadow")

        # F2F reminder
        if self.is_i2p_proxy_active():
            anomalies.append("F2F Tunneling Reminder — Manual Enable in I2P Settings > Advanced > Network > Restricted Routes Mercy")

        if not anomalies:
            logging.info("I2P SAM API + Routing Harmony Pure ∞")

        return anomalies
