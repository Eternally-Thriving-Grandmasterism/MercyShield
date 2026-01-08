import logging
import socket
import time
from jnius import autoclass, JavaException

# Android pyjnius classes
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
Context = autoclass('android.content.Context')
PackageManager = autoclass('android.content.pm.PackageManager')

FREENET_PACKAGE = "org.freenetproject.mobile"

FCP_HOST = "127.0.0.1"
FCP_PORT = 9481  # Default FCP port

class FreenetIntegration:
    """Real Freenet Mobile + FCP Integration Thunder ∞ Pure — Launch + NodeHello Test"""
    def __init__(self, app):
        self.app = app
        self.activity = PythonActivity.mActivity
        self.context = self.activity.getPackageManager()

    def is_freenet_installed(self) -> bool:
        try:
            self.context.getPackageInfo(FREENET_PACKAGE, PackageManager.GET_ACTIVITIES)
            return True
        except JavaException:
            return False

    def launch_freenet(self) -> bool:
        if not self.is_freenet_installed():
            return False
        try:
            intent = Intent(Intent.ACTION_MAIN)
            intent.setPackage(FREENET_PACKAGE)
            intent.addCategory(Intent.CATEGORY_LAUNCHER)
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            self.activity.startActivity(intent)
            logging.info("Freenet Launch Intent Sent Harmony ∞")
            return True
        except Exception as e:
            logging.error(f"Freenet Launch Shadow: {e}")
            return False

    def fcp_hello_test(self) -> bool:
        """FCP ClientHello → NodeHello test"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((FCP_HOST, FCP_PORT))
            hello_msg = "ClientHello\nName=MercyShield\nExpectedVersion=2.0\nEndMessage\n"
            s.send(hello_msg.encode())
            response = b""
            while True:
                data = s.recv(1024)
                if not data:
                    break
                response += data
                if b"EndMessage" in data:
                    break
            s.close()
            response_str = response.decode(errors='ignore')
            if "NodeHello" in response_str and "Freenet" in response_str:
                logging.info("Freenet FCP NodeHello Harmony Pure ∞")
                return True
        except Exception as e:
            logging.warning(f"FCP Hello Shadow: {e}")
        return False

    def full_freenet_verification(self) -> list[str]:
        anomalies = []

        if not self.is_freenet_installed():
            anomalies.append("Freenet Mobile Not Installed — Install from F-Droid (org.freenetproject.mobile) Mercy")

        if not self.fcp_hello_test():
            anomalies.append("Freenet FCP Not Active — Node Shadow Critical")

        if not anomalies:
            logging.info("Freenet FCP Integration Harmony Pure ∞")

        return anomalies
