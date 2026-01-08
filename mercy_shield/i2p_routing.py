import logging
import socket
import requests
from jnius import autoclass, JavaException

# Android pyjnius classes
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
Context = autoclass('android.content.Context')
PackageManager = autoclass('android.content.pm.PackageManager')

I2P_PACKAGE = "net.i2p.android.router"  # Official I2P Android router

class I2PRouting:
    """Real I2P Router + F2F Tunneling Reminder Thunder ∞ Pure — Launch, Proxy, Eepsite + F2F Manual Guide"""
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

    def launch_i2p(self, enable_f2f_reminder: bool = True) -> bool:
        if not self.is_i2p_installed():
            return False
        try:
            intent = Intent(Intent.ACTION_MAIN)
            intent.setPackage(I2P_PACKAGE)
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            self.activity.startActivity(intent)
            logging.info("I2P Launch Intent Sent Harmony ∞")
            if enable_f2f_reminder:
                self.app.ui_feedback("I2P Launched — Enable F2F in Settings > Advanced > Network > Restricted Routes for Friend-to-Friend Tunneling Mercy ∞")
            return True
        except Exception as e:
            logging.error(f"I2P Launch Shadow: {e}")
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
            anomalies.append("I2P Router App Not Installed — Install from F-Droid (net.i2p.android.router) Mercy")

        if not self.is_i2p_proxy_active():
            anomalies.append("I2P Proxy Not Active — Launch & Enable F2F for Restricted Tunneling")

        if not self.i2p_connectivity_test():
            anomalies.append("I2P Eepsite Connectivity Failed — Check F2F/Routing Shadow")

        # F2F reminder anomaly if proxy active but user may need manual enable
        if self.is_i2p_proxy_active():
            anomalies.append("F2F Tunneling Reminder — Manual Enable in I2P Settings > Advanced > Network > Restricted Routes for Friend-to-Friend Mercy")

        if not anomalies:
            logging.info("I2P Routing + F2F Ready Harmony Pure ∞")

        return anomalies
