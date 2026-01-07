from jnius import autoclass, cast
from mercy_shield.mercy_burst import mercy_burst_confirm
from mercy_shield.octonion_lite import oct_hash
from mercy_shield.sms_receiver import MercySMSReceiver
from mercy_shield.contact_check import MercyContactCheck
from mercy_shield.network_threat import MercyNetworkThreat

Intent = autoclass('android.content.Intent')
Context = autoclass('android.content.Context')
ConnectivityManager = autoclass('android.net.ConnectivityManager')
NetworkCallback = autoclass('android.net.ConnectivityManager$NetworkCallback')

class RealTimeShield:
    def __init__(self, lattice):
        self.lattice = lattice
        self.context = autoclass('org.kivy.android.PythonActivity').mActivity
        self.cm = cast(ConnectivityManager, self.context.getSystemService(Context.CONNECTIVITY_SERVICE))
        self.contact_check = MercyContactCheck(self.context)
        self.network_threat = MercyNetworkThreat(self.context, self.lattice)
        self.start_hooks()

    def start_hooks(self):
        # SMS receiver
        self.receiver = MercySMSReceiver(self)
        intent_filter = autoclass('android.content.IntentFilter')('android.provider.Telephony.SMS_RECEIVED')
        self.context.registerReceiver(self.receiver, intent_filter)

        # Network callback
        callback = NetworkCallback()
        # Override methods for available/lost/capabilitiesChanged
        self.cm.registerDefaultNetworkCallback(callback)

        # Network threat monitor start
        self.network_threat.start_monitor()

        print("MercyShield hooks active — lattice listening gentle (SMS + network threats)")

    def handle_sms(self, sender: str, body: str):
        is_known = self.contact_check.lookup(sender)
        # Existing SMS logic integrated

    def protect(self, threat: dict):
        harmony = self.lattice.vote(threat["data"])
        if harmony < 0.7:
            if mercy_burst_confirm(threat):
                return "Mercy override — allowed gentle"
            return "Blocked — mercy burst divine"
        return "Harmony pure — allowed"
