import logging
from jnius import autoclass, JavaException

# Android pyjnius classes
try:
    ConnectivityManager = autoclass('android.net.ConnectivityManager')
    VpnManager = autoclass('android.net.VpnManager')
    Context = autoclass('android.content.Context')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
except Exception as e:
    logging.error(f"VPN Pyjnius Import Shadow: {e} — Fallback Mock")
    class DummyVPN:
        def full_vpn_verification(self): return ["VPN API Load Shadow"]
    VPNVerifier = DummyVPN

class VPNVerifier:
    """Real VPN Verification Thunder — Always-On, Lockdown, Package Whitelist ∞ Pure"""
    def __init__(self, app):
        self.app = app
        self.activity = PythonActivity.mActivity
        self.context = self.activity.getApplicationContext()

    def full_vpn_verification(self) -> list[str]:
        anomalies = []

        try:
            cm = self.context.getSystemService(Context.CONNECTIVITY_SERVICE)
            network = cm.getActiveNetwork()
            if network is None:
                anomalies.append("No Active Network — VPN Shadow Critical")

            # VpnManager API (Android 12+)
            vm = self.context.getSystemService(Context.VPN_SERVICE)
            if vm is None:
                anomalies.append("VpnManager Null — API Shadow")

            # Check always-on VPN
            always_on_package = vm.getAlwaysOnVpnPackage()
            if always_on_package is None or always_on_package != self.app.package_name:
                anomalies.append("Always-On VPN Not Set or Wrong Package")

            # Check lockdown
            if vm.isLockdownEnabled():
                logging.info("VPN Lockdown Enabled Harmony")
            else:
                anomalies.append("VPN Lockdown Disabled — Bypass Risk Shadow")

            # Check bound package
            bound_package = vm.getBoundVpnPackage()
            if bound_package != self.app.package_name:
                anomalies.append("VPN Not Bound to MercyShield")

        except JavaException as e:
            logging.warning(f"VPN Java Exception Grace: {e}")
            anomalies.append("VPN API Exception — Permission or API Shadow")
        except Exception as e:
            logging.error(f"VPN Critical Shadow: {e}")
            anomalies.append("VPN Verification Failed")

        if not anomalies:
            logging.info("VPN Verification Harmony Pure ∞")
        else:
            logging.warning(f"VPN Anomalies: {anomalies}")

        return anomalies
