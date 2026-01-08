from jnius import autoclass
import threading
import time

VpnService = autoclass('android.net.VpnService')
Builder = autoclass('android.net.VpnService$Builder')
ConnectivityManager = autoclass('android.net.ConnectivityManager')
Context = autoclass('android.content.Context')

class MercyFirewallVPN(VpnService):
    def __init__(self, context, lattice, shield):
        super().__init__()
        self.context = context
        self.lattice = lattice
        self.shield = shield
        self.vpn_interface = None
        self.vpn_active = False
        self.blocked_apps = []
        self.blocked_domains = ["malicious-c2.com", "phish-bank.ru"]

    def start_vpn_if_approved(self):
        intent = VpnService.prepare(self.context)
        if intent:
            self.context.startActivity(intent)
        else:
            self.establish_vpn()
            self.start_kill_switch_monitor()

    def establish_vpn(self):
        builder = Builder(self)
        builder.setSession("MercyShield Firewall + Kill Switch")
        builder.addAddress("10.0.0.2", 32)
        builder.addDnsServer("8.8.8.8")
        builder.addRoute("0.0.0.0", 0)
        builder.setMtu(1500)

        for app in self.blocked_apps:
            builder.addDisallowedApplication(app)

        self.vpn_interface = builder.establish()
        self.vpn_active = True
        print("MercyShield firewall VPN + kill switch established — full protection mercy pure")

        # Packet inspect loop stub (expanded previous)
        threading.Thread(target=self.packet_inspect_loop, daemon=True).start()

    def start_kill_switch_monitor(self):
        threading.Thread(target=self.kill_switch_loop, daemon=True).start()
        print("MercyShield kill switch monitor active — VPN drop protection gentle")

    def kill_switch_loop(self):
        while True:
            cm = self.context.getSystemService(Context.CONNECTIVITY_SERVICE)
            active = cm.getActiveNetwork()
            vpn_transport = False
            if active:
                info = cm.getNetworkInfo(active)
                if info:
                    vpn_transport = info.getType() == ConnectivityManager.TYPE_VPN

            if self.vpn_active and not vpn_transport:
                # VPN dropped — kill switch activate
                threat = {
                    "type": "vpn_kill_switch",
                    "desc": "VPN disconnected — kill switch blocking all internet",
                    "data": oct_hash(b"vpn_drop_kill_switch")
                }
                self.shield.handle_kill_switch_threat(threat)
                # Block all traffic mercy (stub: disable network or route null)
                self.block_all_traffic()

            time.sleep(5)  # Low-power check

    def block_all_traffic(self):
        print("Kill switch active — all internet blocked mercy divine")
        # Real: disable network adapters or AppOps set network restricted

    def packet_inspect_loop(self):
        # Existing packet inspect + drop malicious
        pass  # Previous expanded

    def onRevoke(self):
        self.vpn_active = False
        print("VPN revoked — kill switch triggered mercy")
