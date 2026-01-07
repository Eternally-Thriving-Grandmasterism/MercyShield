from jnius import autoclass
from mercy_shield.octonion_lite import oct_hash

ConnectivityManager = autoclass('android.net.ConnectivityManager')
NetworkStatsManager = autoclass('android.app.usage.NetworkStatsManager')
Context = autoclass('android.content.Context')
UidStats = autoclass('android.app.usage.NetworkStats$Bucket')

class RealTimeShield:
    def __init__(self, lattice):
        self.lattice = lattice
        self.context = autoclass('org.kivy.android.PythonActivity').mActivity
        self.ns_manager = self.context.getSystemService(Context.NETWORK_STATS_SERVICE)
        self.start_network_monitor()

    def start_network_monitor(self):
        # Periodic query (every 60s low-power) or callback if API allows
        import threading
        threading.Timer(60.0, self.check_exfil).start()
        print("MercyShield network exfil monitor active — data flow rhythm listening gentle")

    def check_exfil(self):
        # Query recent stats (last 5min stub)
        end = System.currentTimeMillis()
        start = end - 300000  # 5min
        stats = self.ns_manager.querySummaryForDevice(ConnectivityManager.TYPE_WIFI, "", start, end)
        # Real: loop per UID/app
        suspicious = False
        if stats and stats.getRxBytes() < stats.getTxBytes() * 5:  # Outbound heavy rhythm
            suspicious = True
        # Host/port stub from active sockets (advanced: use /proc/net/tcp)

        if suspicious:
            threat = {
                "type": "network_exfil",
                "desc": f"Data exfil shadow — high outbound burst detected",
                "data": oct_hash(str(stats).encode())
            }
            action = self.protect(threat)
            print(f"Exfil threat: {action}")

        # Restart timer
        threading.Timer(60.0, self.check_exfil).start()
