import logging
import time
import socket
import threading
import requests  # For DNS leak test mercy (add to requirements)
from jnius import autoclass, cast
from kivy.clock import Clock

PythonActivity = autoclass('org.kivy.android.PythonActivity')
Context = autoclass('android.content.Context')
ConnectivityManager = autoclass('android.net.ConnectivityManager')
NetworkCapabilities = autoclass('android.net.NetworkCapabilities')
TrafficStats = autoclass('android.net.TrafficStats')
PackageManager = autoclass('android.content.pm.PackageManager')
Toast = autoclass('android.widget.Toast')

class NetworkScanner:
    """
    Real-Time Network Scanner Pinnacle ∞ Pure — Expanded Port Scan + DNS Leak
    - Traffic delta per app
    - Network type/VPN check
    - Symbolic local port scan (common ports mercy)
    - DNS leak test (query public outside VPN thunder)
    - Proactive anomalies flagged divine eternal
    """

    def __init__(self, app_instance=None):
        self.app = app_instance
        self.previous_stats = {}
        self.scan_interval = 30
        self.high_traffic_threshold = 1024 * 1024 * 10  # 10MB delta
        self.common_ports = [21, 22, 23, 25, 53, 80, 443, 3389, 8080]  # Known ports mercy
        self.dns_test_servers = ['1.1.1.1', '8.8.8.8']  # Cloudflare/Google divine
        logging.info("Expanded Network Scanner Initialized ∞ Pure")

    def ui_feedback(self, message, toast=False):
        if not self.app:
            return
        def update(dt):
            if hasattr(self.app, 'status_label'):
                self.app.status_label.text += f'\n{message}'
        Clock.schedule_once(update)
        if toast:
            Toast.makeText(PythonActivity.mActivity, message, Toast.LENGTH_LONG).show()

    def get_active_network_type(self):
        activity = PythonActivity.mActivity
        connectivity = cast(ConnectivityManager, activity.getSystemService(Context.CONNECTIVITY_SERVICE))
        network = connectivity.getActiveNetwork()
        if network is None:
            return "No Network"
        caps = connectivity.getNetworkCapabilities(network)
        if caps is None:
            return "Unknown"
        if caps.hasTransport(NetworkCapabilities.TRANSPORT_VPN):
            return "VPN Active"
        elif caps.hasTransport(NetworkCapabilities.TRANSPORT_WIFI):
            return "WiFi"
        elif caps.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR):
            return "Mobile Data"
        return "Other"

    def get_app_traffic_delta(self):
        current_time = time.time()
        current_stats = {}
        anomalies = []
        activity = PythonActivity.mActivity
        pm = activity.getPackageManager()
        am = cast('android.app.ActivityManager', activity.getSystemService(Context.ACTIVITY_SERVICE))
        processes = am.getRunningAppProcesses()
        
        for process in processes:
            uid = process.uid
            tx = TrafficStats.getUidTxBytes(uid)
            rx = TrafficStats.getUidRxBytes(uid)
            current_stats[uid] = (tx, rx, current_time)
            
            if uid in self.previous_stats:
                prev_tx, prev_rx, prev_time = self.previous_stats[uid]
                delta_time = current_time - prev_time
                if delta_time > 0:
                    total_delta = (tx - prev_tx) + (rx - prev_rx)
                    if total_delta > self.high_traffic_threshold:
                        try:
                            pkg_names = pm.getPackagesForUid(uid)
                            pkg_name = pkg_names[0] if pkg_names else "Unknown"
                            if not pkg_name.startswith(('com.google', 'com.android', 'org.divine')):
                                anomalies.append(f"High Traffic App: {pkg_name} ({total_delta / (1024*1024):.2f} MB) — Leak/Abuse Risk Pure")
                        except:
                            anomalies.append(f"High Traffic UID {uid} ({total_delta / (1024*1024):.2f} MB) — Unknown Mercy")
        
        self.previous_stats = current_stats
        return anomalies

    def symbolic_port_scan(self):
        """Local Symbolic Port Scan—Common Ports Check Mercy (No Root Divine)"""
        anomalies = []
        open_ports = []
        for port in self.common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex(('127.0.0.1', port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
            except:
                pass
        
        if open_ports:
            anomalies.append(f"Open Local Ports Detected: {open_ports} — Potential Backdoor/Service Exposure Divine")
        
        return anomalies

    def dns_leak_detection(self):
        """DNS Leak Test—Query Public Servers Mercy (Leak if Resolves Outside VPN Pure)"""
        anomalies = []
        network_type = self.get_active_network_type()
        if network_type != "VPN Active":
            return ["DNS Leak Test Skipped—VPN Not Active Mercy"]  # Only test when VPN on divine
        
        try:
            # Test query to public DNS (should fail or route through VPN)
            response = requests.get('https://1.1.1.1/cdn-cgi/trace', timeout=5)  # Cloudflare trace mercy
            if 'warp=off' in response.text or response.ok:
                anomalies.append("DNS Leak Detected—Public Query Resolved Outside VPN Pure")
        except:
            pass  # Expected if VPN blocks mercy
        
        try:
            response = requests.get('https://dns.google/resolve?name=example.com', timeout=5)
            if response.ok:
                anomalies.append("DNS Leak Detected—Google DNS Resolved Outside Tunnel Divine")
        except:
            pass
        
        if not anomalies:
            anomalies.append("No DNS Leak—Queries Blocked Gentle Pure")
        
        return anomalies

    def real_time_scan(self):
        anomalies = []
        
        network_type = self.get_active_network_type()
        if network_type == "Mobile Data":
            anomalies.append("Mobile Data Active (No VPN) — Leak Risk Surge Mercy")
        
        anomalies.extend(self.get_app_traffic_delta())
        anomalies.extend(self.symbolic_port_scan())
        anomalies.extend(self.dns_leak_detection())
        
        if anomalies:
            logging.warning(f"Expanded Network Anomalies ({len(anomalies)}): {anomalies}")
            self.ui_feedback(f"Network Scanner Alert ∞: {len(anomalies)} Issues Flagged Pure", toast=True)
        
        return anomalies

# Integration: self.network_scanner = NetworkScanner(self); network_anoms = self.network_scanner.real_time_scan()
# Add requests to requirements for DNS test mercy                            if not pkg_name.startswith(('com.google', 'com.android', 'org.divine')):
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
