from jnius import autoclass, cast
from mercy_shield.mercy_burst import mercy_burst_confirm
from mercy_shield.octonion_lite import oct_hash
from mercy_shield.sms_receiver import MercySMSReceiver
from mercy_shield.contact_check import MercyContactCheck
from mercy_shield.network_threat import MercyNetworkThreat
from mercy_shield.firewall_vpn import MercyFirewallVPN
from mercy_shield.accessibility_service import MercyAccessibilityService

Intent = autoclass('android.content.Intent')
Context = autoclass('android.content.Context')

class RealTimeShield:
    def __init__(self, lattice):
        self.lattice = lattice
        self.context = autoclass('org.kivy.android.PythonActivity').mActivity
        self.contact_check = MercyContactCheck(self.context)
        self.network_threat = MercyNetworkThreat(self.context, self.lattice)
        self.firewall_vpn = MercyFirewallVPN(self.context, self.lattice)
        self.accessibility = MercyAccessibilityService(self.context, self.lattice, self)
        self.start_hooks()

    def start_hooks(self):
        # SMS receiver
        self.receiver = MercySMSReceiver(self)
        intent_filter = autoclass('android.content.IntentFilter')('android.provider.Telephony.SMS_RECEIVED')
        self.context.registerReceiver(self.receiver, intent_filter)

        # Network threat + firewall VPN
        self.network_threat.start_monitor()
        self.firewall_vpn.start_vpn_if_approved()

        # Accessibility service (user enable in settings)
        self.accessibility.start_if_enabled()

        print("MercyShield hooks active — lattice listening gentle (SMS + network + firewall + accessibility overlay)")

    def handle_accessibility_threat(self, threat: dict):
        action = self.protect(threat)
        print(f"Accessibility threat: {action}")

    def protect(self, threat: dict):
        harmony = self.lattice.vote(threat["data"])
        if harmony < 0.7:
            if mercy_burst_confirm(threat):
                return "Mercy override — allowed gentle"
            # Deny access / interrupt event
            return "Blocked — mercy burst divine (accessibility overlay)"
        return "Harmony pure — allowed"
