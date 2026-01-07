from jnius import autoclass, cast
from mercy_shield.mercy_burst import mercy_burst_confirm
from mercy_shield.octonion_lite import oct_hash
from mercy_shield.sms_receiver import MercySMSReceiver
from mercy_shield.contact_check import MercyContactCheck
from mercy_shield.network_threat import MercyNetworkThreat
from mercy_shield.firewall_vpn import MercyFirewallVPN

Intent = autoclass('android.content.Intent')
Context = autoclass('android.content.Context')

class RealTimeShield:
    def __init__(self, lattice):
        self.lattice = lattice
        self.context = autoclass('org.kivy.android.PythonActivity').mActivity
        self.contact_check = MercyContactCheck(self.context)
        self.network_threat = MercyNetworkThreat(self.context, self.lattice)
        self.firewall_vpn = MercyFirewallVPN(self.context, self.lattice)
        self.start_hooks()

    def start_hooks(self):
        # SMS receiver
        self.receiver = MercySMSReceiver(self)
        intent_filter = autoclass('android.content.IntentFilter')('android.provider.Telephony.SMS_RECEIVED')
        self.context.registerReceiver(self.receiver, intent_filter)

        # Network threat + firewall VPN start
        self.network_threat.start_monitor()
        self.firewall_vpn.start_vpn_if_approved()  # User opt-in VPN setup

        print("MercyShield hooks active — lattice listening gentle (SMS + network + firewall VPN)")

    def protect(self, threat: dict):
        harmony = self.lattice.vote(threat["data"])
        if harmony < 0.7:
            if mercy_burst_confirm(threat):
                return "Mercy override — allowed gentle"
            # Firewall block via VPN drop packet
            return "Blocked — mercy burst divine (firewall rule)"
        return "Harmony pure — allowed"
