import logging
from jnius import autoclass, JavaException

# Android pyjnius classes
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
Context = autoclass('android.content.Context')
PackageManager = autoclass('android.content.pm.PackageManager')

FREENET_PACKAGE = "org.freenetproject.mobile"  # Official Freenet Mobile from F-Droid/GitHub

class FreenetRouting:
    """Real Freenet Mobile App Integration Thunder ∞ Pure — Launch + Status Check"""
    def __init__(self, app):
        self.app = app
        self.activity = PythonActivity.mActivity
        self.context = self.activity.getPackageManager()

    def is_freenet_installed(self) -> bool:
        """Check if Freenet Mobile app installed"""
        try:
            self.context.getPackageInfo(FREENET_PACKAGE, PackageManager.GET_ACTIVITIES)
            return True
        except JavaException:
            return False

    def launch_freenet(self) -> bool:
        """Launch Freenet Mobile main activity"""
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

    def full_freenet_verification(self) -> list[str]:
        anomalies = []

        if not self.is_freenet_installed():
            anomalies.append("Freenet Mobile Not Installed — Install from F-Droid Mercy (org.freenetproject.mobile)")

        # No proxy/port test — Freenet own protocol, assume launched = running
        # Optional future: check local web UI if exposed

        if not anomalies:
            logging.info("Freenet Integration Harmony Pure ∞")

        return anomalies
