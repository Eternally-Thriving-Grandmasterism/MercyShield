import logging
import time
from jnius import autoclass, cast
from kivy.clock import Clock

PythonActivity = autoclass('org.kivy.android.PythonActivity')
Context = autoclass('android.content.Context')
ConnectivityManager = autoclass('android.net.ConnectivityManager')
NetworkStatsManager = autoclass('android.app.usage.NetworkStatsManager')
TrafficStats = autoclass('android.net.TrafficStats')
PackageManager = autoclass('android.content.pm.PackageManager')

class NetworkScanner:
    """
    Real-Time Network Scanner Pinnacle ∞ Pure
    - Monitor active network type (WiFi/Mobile/VPN mercy)
    - Traffic stats per app (delta rate divine)
    - Flag high usage unknown apps, sudden spikes, no VPN on mobile
    - Integrate watchdog/council—proactive leak/anomaly detection eternal
    """

    def __init__(self, app_instance=None):
        self.app = app_instance
        self.previous_stats = {}  # {uid: (tx, rx, timestamp)}
        self.scan_interval = 30  # Seconds mercy
        self.high_traffic_threshold = 1024 * 1024 * 10  # 10MB delta gentle (adjust divine)
        logging.info("Real-Time Network Scanner Initialized ∞ Pure")

    def ui_feedback(self, message, toast=False):
        if not self.app:
            return
        def update(dt):
            if hasattr(self.app, 'status_label'):
                self.app.status_label.text += f'\n{message}'
        Clock.schedule_once(update)
        if toast:
            Toast = autoclass('android.widget.Toast')
            Toast.makeText(PythonActivity.mActivity, message, Toast.LENGTH_LONG).show()

    def get_active_network_type(self):
        """Active Network Type + VPN Check Mercy"""
        activity = PythonActivity.mActivity
        connectivity = cast(ConnectivityManager, activity.getSystemService(Context.CONNECTIVITY_SERVICE))
        network = connectivity.getActiveNetwork()
        if network is None:
            return "No Network"
        capabilities = connectivity.getNetworkCapabilities(network)
        if capabilities is None:
            return "Unknown"
        # Simplified VPN check (capabilities has TRANSPORT_VPN mercy)
        if capabilities.hasTransport(capabilities.TRANSPORT_VPN):
            return "VPN Active"
        elif capabilities.hasTransport(capabilities.TRANSPORT_WIFI):
            return "WiFi"
        elif capabilities.hasTransport(capabilities.TRANSPORT_CELLULAR):
            return "Mobile Data"
        return "Other"

    def get_app_traffic_delta(self):
        """Traffic Delta Per App Since Last Scan Divine"""
        current_time = time.time()
        current_stats = {}
        anomalies = []
        activity = PythonActivity.mActivity
        pm = activity.getPackageManager()
        
        # Get running app UIDs (approximate mercy)
        am = cast('android.app.ActivityManager', activity.getSystemService(Context.ACTIVITY_SERVICE))
        running_processes = am.getRunningAppProcesses()
        
        for process in running_processes:
            uid = process.uid
            tx = TrafficStats.getUidTxBytes(uid)
            rx = TrafficStats.getUidRxBytes(uid)
            current_stats[uid] = (tx, rx, current_time)
            
            if uid in self.previous_stats:
                prev_tx, prev_rx, prev_time = self.previous_stats[uid]
                delta_time = current_time - prev_time
                if delta_time > 0:
                    tx_rate = (tx - prev_tx) / delta_time  # Bytes/sec
                    rx_rate = (rx - prev_rx) / delta_time
                    total_delta = tx - prev_tx + rx - prev_rx
                    if total_delta > self.high_traffic_threshold:
                        try:
                            pkg_names = pm.getPackagesForUid(uid)
                            pkg_name = pkg_names[0] if pkg_names else "Unknown"
                            if not pkg_name.startswith(('com.google', 'com.android', 'org.divine')):
                                anomalies.append(f"High Network Traffic App: {pkg_name} ({total_delta / (1024*1024):.2f} MB) — Potential Leak/Background Abuse Divine")
                        except:
                            anomalies.append(f"High Traffic UID {uid} ({total_delta / (1024*1024):.2f} MB) — Unknown App Mercy")
        
        self.previous_stats = current_stats
        return anomalies

    def real_time_scan(self):
        """Full Real-Time Scan Call—Return Anomalies Mercy"""
        anomalies = []
        
        network_type = self.get_active_network_type()
        if network_type == "Mobile Data":
            anomalies.append("Mobile Data Active (No VPN) — Potential Leak Risk Mercy Pure")
        elif network_type == "No Network":
            anomalies.append("No Active Network — Offline or Tunnel Down Divine")
        
        traffic_anoms = self.get_app_traffic_delta()
        anomalies.extend(traffic_anoms)
        
        if anomalies:
            logging.warning(f"Real-Time Network Anomalies ({len(anomalies)}): {anomalies}")
            self.ui_feedback(f"Network Scanner Alert ∞: {len(anomalies)} Issues Flagged Pure", toast=True)
        
        return anomalies

# Integration: In watchdog monitor—self.network_scanner = NetworkScanner(self); network_anoms = self.network_scanner.real_time_scan(); anomalies.extend(network_anoms)
# Call periodically in thread mercy
