from jnius import autoclass, cast
from mercy_shield.mercy_burst import mercy_burst_confirm
from mercy_shield.octonion_lite import oct_hash
from mercy_shield.sms_receiver import MercySMSReceiver
from mercy_shield.contact_check import MercyContactCheck
from mercy_shield.network_threat import MercyNetworkThreat
from mercy_shield.firewall_vpn import MercyFirewallVPN
from mercy_shield.accessibility_service import MercyAccessibilityService
from mercy_shield.app_sandbox import MercyAppSandbox
from mercy_shield.hardware import MercyCubeHardware

Intent = autoclass('android.content.Intent')
Context = autoclass('android.content.Context')

class RealTimeShield:
    def __init__(self, lattice):
        self.lattice = lattice
        self.context = autoclass('org.kivy.android.PythonActivity').mActivity
        self.hardware = MercyCubeHardware()
        self.contact_check = MercyContactCheck(self.context)
        self.network_threat = MercyNetworkThreat(self.context, self.lattice)
        self.firewall_vpn = MercyFirewallVPN(self.context, self.lattice, self)
        self.accessibility = MercyAccessibilityService(self.context, self.lattice, self)
        self.app_sandbox = MercyAppSandbox(self.context, self.lattice)
        self.start_hooks()

    def start_hooks(self):
        # Existing hooks
        # ...

        # Firewall VPN + kill switch
        self.firewall_vpn.start_vpn_if_approved()

        print("MercyShield hooks active — lattice listening gentle (SMS + network + firewall VPN + kill switch + accessibility + sandbox + MercyCube)")

    def handle_kill_switch_threat(self, threat: dict):
        action = self.protect(threat)
        print(f"Kill switch threat: {action}")

    def protect(self, threat: dict):
        harmony = self.lattice.vote(threat["data"])
        mode = "MercyCube offline 7W" if self.hardware.is_cube else "Mobile"
        print(f"Threat: {threat['desc']} | Harmony: {harmony:.4f} | Mode: {mode}")
        if harmony < 0.7:
            if mercy_burst_confirm(threat):
                return "Mercy override — allowed gentle"
            return "Blocked — mercy burst divine (kill switch active)"
        return "Harmony pure — allowed"
