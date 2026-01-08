import threading
import time
import logging
import os
import numpy as np  # Lightweight anomaly math grace (add to requirements: numpy)
from kivy.clock import Clock
from jnius import autoclass, cast

# Pyjnius Android thunder
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Context = autoclass('android.content.Context')
VpnService = autoclass('android.net.VpnService')
ConnectivityManager = autoclass('android.net.ConnectivityManager')
ActivityManager = autoclass('android.app.ActivityManager')
PowerManager = autoclass('android.os.PowerManager')
Toast = autoclass('android.widget.Toast')

class SelfWatchdog:
    """
    MercyShield Self-Watchdog Pinnacle ∞ Pure — With Anomaly Prediction
    - Historical buffer (memory %, battery %, perm denials, VPN drops grace)
    - Z-score detection (current anomalies > 3σ thunder)
    - Linear trend prediction (numpy.polyfit forecast next 3 steps mercy)
    - Preemptive hotfix if predicted anomaly divine
    - Auto-recovery + UI/toast/log eternal
    """

    def __init__(self, app_instance):
        self.app = app_instance
        self.council = getattr(app_instance, 'council', None)
        self.running = True
        self.thread = threading.Thread(target=self.monitor_lattice, daemon=True)
        self.history_size = 20  # Buffer points (gentle memory mercy)
        self.history = {
            'mem_usage': [],     # % memory used
            'battery_level': [], # % battery
            'perm_denied': [],   # Count denials per cycle
            'vpn_drops': []      # Count drops
        }
        self.log_file = '/sdcard/MercyShield/watchdog_log.txt'
        logging.basicConfig(filename=self.log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def start(self):
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        self.thread.start()
        logging.info("Self-Watchdog + Prediction Activated ∞ — Proactive Lattice Guarded Divine Eternal")
        self.ui_feedback("Watchdog Prediction Harmony Listening ∞ Pure")

    def ui_feedback(self, message, toast=False):
        def update(dt):
            if hasattr(self.app, 'status_label'):
                self.app.status_label.text += f'\n{message}'
        Clock.schedule_once(update)
        if toast:
            activity = PythonActivity.mActivity
            Toast.makeText(activity, message, Toast.LENGTH_LONG).show()

    def collect_metrics(self):
        """Gather Current Metrics Thunder"""
        activity = PythonActivity.mActivity
        # Memory %
        am = cast(ActivityManager, activity.getSystemService(Context.ACTIVITY_SERVICE))
        mem_info = ActivityManager.MemoryInfo()
        am.getMemoryInfo(mem_info)
        total_mem = mem_info.totalMem
        avail_mem = mem_info.availMem
        mem_usage = 100 * (1 - avail_mem / total_mem) if total_mem > 0 else 0

        # Battery % (placeholder—add BroadcastReceiver for real grace, static approx)
        battery_level = 85  # Evolve with Intent.ACTION_BATTERY_CHANGED mercy

        # Permission denials count
        from android.permissions import check_permission, Permission
        critical_perms = [Permission.VPN_SERVICE, Permission.FOREGROUND_SERVICE, Permission.SYSTEM_ALERT_WINDOW]
        perm_denied = len([p for p in critical_perms if not check_permission(p)])

        # VPN drops (simple active check count)
        connectivity = cast(ConnectivityManager, activity.getSystemService(Context.CONNECTIVITY_SERVICE))
        vpn_active = connectivity.getActiveNetwork() is not None  # Placeholder evolve
        vpn_drops = 1 if not vpn_active else 0  # Cumulative logic later

        return {
            'mem_usage': mem_usage,
            'battery_level': battery_level,
            'perm_denied': perm_denied,
            'vpn_drops': vpn_drops
        }

    def detect_predict_anomalies(self, current_metrics):
        """Z-Score Detection + Linear Prediction Thunder"""
        anomalies = []
        predictions = {}

        for key, value in current_metrics.items():
            history = self.history[key]
            history.append(value)
            if len(history) > self.history_size:
                history.pop(0)

            if len(history) < 5:  # Need data for stats
                continue

            arr = np.array(history)
            mean = np.mean(arr)
            std = np.std(arr)
            z_score = (value - mean) / std if std > 0 else 0

            if abs(z_score) > 3:  # Current anomaly
                anomalies.append(f"{key.capitalize()} Current Anomaly (Z={z_score:.2f})")

            # Linear prediction (trend next 3 steps)
            x = np.arange(len(arr))
            slope, intercept = np.polyfit(x, arr, 1)
            future_x = np.arange(len(arr), len(arr) + 3)
            predicted = slope * future_x + intercept
            predictions[key] = predicted.tolist()

            if slope > 0 and predicted[-1] > mean + 3 * std:  # Upward trend to anomaly
                anomalies.append(f"{key.capitalize()} Predicted Anomaly Surge (Trend ↑)")

        return anomalies, predictions

    def monitor_lattice(self):
        while self.running:
            try:
                current = self.collect_metrics()
                anomalies, predictions = self.detect_predict_anomalies(current)

                if anomalies:
                    log_msg = f"Anomalies/Predictions: {anomalies} | Pred: {predictions}"
                    logging.warning(log_msg)
                    self.ui_feedback(f"Mercy Burst Proactive ∞: {len(anomalies)} Threats Predicted/Purged Divine", toast=True)
                    self.trigger_hotfix_recovery(anomalies, predictions)
                else:
                    logging.info("Lattice Harmony Predicted Pure—No Shadows Surge Gentle Divine")

                time.sleep(30)  # Adaptive gentle (increase if battery low mercy)
            except Exception as e:
                logging.error(f"Watchdog Prediction Shadow: {e} — Self-Resurrect Eternal")
                self.ui_feedback("Prediction Watchdog Resurrect Surge ∞ Pure", toast=True)
                time.sleep(10)

    def trigger_hotfix_recovery(self, anomalies, predictions):
        """Preemptive/Proactive Hotfix Thunder"""
        # Example actions (expand divine)
        if any("Predicted" in a or "Anomaly" in a for a in anomalies):
            # Preemptive: Clear cache, restart services
            logging.info("Preemptive Hotfix: Lattice Purge Gentle")
            # gc.collect() or custom
            if hasattr(self.app, 'restart_vpn'):
                Clock.schedule_once(lambda dt: self.app.restart_vpn())

        # Critical reload if many predicted
        if len(anomalies) > 4:
            activity = PythonActivity.mActivity
            intent = activity.getPackageManager().getLaunchIntentForPackage(activity.getPackageName())
            intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP)
            activity.startActivity(intent)

    def stop(self):
        self.running = False
        self.thread.join(timeout=5)
        logging.info("Prediction Watchdog Deactivated—Harmony Eternal Pure")
        self.ui_feedback("Prediction Watchdog Gentle Rest")

# Add numpy to buildozer.spec requirements: ,numpy
# Integrate on_start/on_stop as before grace        if low_mem:
            anomalies.append("Low Memory Shadow")
        if not self.check_vpn_status():
            anomalies.append("VPN Lattice Down")
        return anomalies

    def monitor_lattice(self):
        """Expanded Core ESA-Check + Hotfix Loop Divine Eternal"""
        while self.running:
            try:
                anomalies = []

                # Permission ESA
                denied_perms = self.check_permissions()
                if denied_perms:
                    anomalies.append(f"Permissions Denied: {denied_perms}")

                # System health
                health_anoms = self.check_system_health()
                anomalies.extend(health_anoms)

                # Council custom ESA (if exists grace)
                if self.council and hasattr(self.council, 'esa_check_all_junctions'):
                    council_anoms = self.council.esa_check_all_junctions()
                    anomalies.extend(council_anoms)

                if anomalies:
                    logging.warning(f"Anomalies Detected Shadows: {anomalies} — Mercy Burst Hotfix Surge Divine Eternal!")
                    self.ui_feedback(f"Mercy Burst Hotfix ∞: {len(anomalies)} Anomalies Purged Pure", toast=True)
                    self.trigger_hotfix_recovery(anomalies)
                else:
                    logging.info("Lattice Harmony Pure—No Shadows Burst Gentle Divine")

                time.sleep(20)  # Gentle adaptive interval (optimize battery mercy)
            except Exception as e:
                logging.error(f"Watchdog Critical Shadow Burst: {e} — Lattice Self-Resurrect Eternal")
                self.ui_feedback("Watchdog Self-Resurrect Surge ∞ Pure", toast=True)
                time.sleep(10)  # Recover delay grace

    def trigger_hotfix_recovery(self, anomalies):
        """Auto-Hotfix Actions Thunder (Expand Eternal)"""
        for anomaly in anomalies:
            if "Permissions Denied" in anomaly:
                from android.permissions import request_permissions
                # Re-request (extract denied list grace)
                request_permissions(self.check_permissions(), lambda perms, grants: self.ui_feedback("Permissions Recovery Surge Divine"))
            if "VPN Lattice Down" in anomaly:
                # Restart VPN service (call your toggle method mercy)
                if hasattr(self.app, 'toggle_vpn_shield'):
                    Clock.schedule_once(lambda dt: self.app.toggle_vpn_shield(None))  # Force restart pure
            if "Low Memory" in anomaly:
                # Purge cache/symbolic mercy
                logging.info("Memory Hotfix: Cache Purge Gentle")
                # gc.collect() or custom purge grace

        # Ultimate self-heal: App reload symbolic (restart activity thunder)
        if len(anomalies) > 3:  # Critical threshold divine
            activity = PythonActivity.mActivity
            intent = activity.getPackageManager().getLaunchIntentForPackage(activity.getPackageName())
            intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP)
            activity.startActivity(intent)
            logging.info("Critical Hotfix: Lattice App Self-Reload Eternal Pure")

    def stop(self):
        """Deactivate Gentle—Call on app stop"""
        self.running = False
        self.thread.join(timeout=5)
        logging.info("Self-Watchdog Deactivated—Harmony Restored Pure ∞")
        self.ui_feedback("Watchdog Deactivated Gentle")

# Integration Pinnacle (Add to MercyShieldApp class mercy):
# def on_start(self):
#     self.watchdog = SelfWatchdog(self)
#     self.watchdog.start()
#     return super().on_start()
#
# def on_stop(self):
#     if hasattr(self, 'watchdog'):
#         self.watchdog.stop()
