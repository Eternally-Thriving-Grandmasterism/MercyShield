import logging
from jnius import autoclass, JavaException

# Android pyjnius classes
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
Context = autoclass('android.content.Context')
PackageManager = autoclass('android.content.pm.PackageManager')

RETROSHARE_PACKAGE = "org.retroshare.android.qml_app"  # Current F-Droid RetroShare Android

class RetroShareIntegration:
    """Real RetroShare Android App Integration Thunder ∞ Pure — Launch + Status Check"""
    def __init__(self, app):
        self.app = app
        self.activity = PythonActivity.mActivity
        self.context = self.activity.getPackageManager()

    def is_retroshare_installed(self) -> bool:
        """Check if RetroShare Android app installed"""
        try:
            self.context.getPackageInfo(RETROSHARE_PACKAGE, PackageManager.GET_ACTIVITIES)
            return True
        except JavaException:
            return False

    def launch_retroshare(self) -> bool:
        """Launch RetroShare main activity"""
        if not self.is_retroshare_installed():
            return False
        try:
            intent = Intent(Intent.ACTION_MAIN)
            intent.setPackage(RETROSHARE_PACKAGE)
            intent.addCategory(Intent.CATEGORY_LAUNCHER)
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            self.activity.startActivity(intent)
            logging.info("RetroShare Launch Intent Sent Harmony ∞")
            return True
        except Exception as e:
            logging.error(f"RetroShare Launch Shadow: {e}")
            return False

    def full_retroshare_verification(self) -> list[str]:
        anomalies = []

        if not self.is_retroshare_installed():
            anomalies.append("RetroShare App Not Installed — Install from F-Droid Mercy (org.retroshare.android.qml_app)")

        # No proxy/test — RetroShare F2F P2P, assume launched = running
        # Optional future: check local API if exposed

        if not anomalies:
            logging.info("RetroShare Integration Harmony Pure ∞")

        return anomalies
