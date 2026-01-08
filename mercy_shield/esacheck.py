import logging
import os
import hashlib
from jnius import autoclass, cast
from kivy.clock import Clock

PythonActivity = autoclass('org.kivy.android.PythonActivity')
Context = autoclass('android.content.Context')
ActivityManager = autoclass('android.app.ActivityManager')
ConnectivityManager = autoclass('android.net.ConnectivityManager')
Toast = autoclass('android.widget.Toast')

class ESAChecker:
    """
    Modular ESA-Checker Pinnacle ∞ Pure — Local Vectors + Integrity + YARA Symbolic
    - Filesystem integrity hashes (tamper detect divine)
    - YARA-like rule symbolic (permission/pattern checks gentle)
    - All Android user-level vectors monitored proactive eternal
    """

    def __init__(self, app_instance=None):
        self.app = app_instance
        self.integrity_baseline = {}
        self.baseline_file = '/sdcard/MercyShield/integrity_baseline.txt'
        self.load_baseline()

    def ui_feedback(self, message, toast=False):
        if not self.app:
            return
        def update(dt):
            if hasattr(self.app, 'status_label'):
                self.app.status_label.text += f'\n{message}'
        Clock.schedule_once(update)
        if toast:
            Toast.makeText(PythonActivity.mActivity, message, Toast.LENGTH_LONG).show()

    def load_baseline(self):
        if os.path.exists(self.baseline_file):
            try:
                with open(self.baseline_file, 'r') as f:
                    for line in f:
                        if ':' in line:
                            path, hash_val = line.strip().split(':', 1)
                            self.integrity_baseline[path] = hash_val
            except Exception as e:
                logging.error(f"Baseline load error: {e}")
        else:
            self.compute_baseline()

    def compute_baseline(self):
        key_paths = []
        activity = PythonActivity.mActivity
        try:
            key_paths.append(activity.getFilesDir().getAbsolutePath())
            key_paths.append('/sdcard/MercyShield/')
            # Add app data if accessible (user-level limited mercy)
        except:
            pass
        
        for path in key_paths:
            if os.path.exists(path):
                hash_val = self.hash_path(path)
                self.integrity_baseline[path] = hash_val
        self.save_baseline()

    def save_baseline(self):
        os.makedirs(os.path.dirname(self.baseline_file), exist_ok=True)
        try:
            with open(self.baseline_file, 'w') as f:
                for path, hash_val in self.integrity_baseline.items():
                    f.write(f"{path}:{hash_val}\n")
        except Exception as e:
            logging.error(f"Baseline save error: {e}")

    def hash_path(self, path):
        sha256 = hashlib.sha256()
        try:
            if os.path.isfile(path):
                with open(path, 'rb') as f:
                    for block in iter(lambda: f.read(4096), b""):
                        sha256.update(block)
            else:
                for root, _, files in os.walk(path):
                    for file in sorted(files):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'rb') as f:
                            for block in iter(lambda: f.read(4096), b""):
                                sha256.update(block)
        except:
            pass
        return sha256.hexdigest()

    def check_filesystem_integrity(self):
        anomalies = []
        for path in self.integrity_baseline:
            if os.path.exists(path):
                current = self.hash_path(path)
                if current != self.integrity_baseline[path]:
                    anomalies.append(f"Filesystem Tamper Detected: {path} — Integrity Shadow Burst Divine!")
        return anomalies

    def yara_like_rule_scan(self):
        anomalies = []
        high_risk_perms = ['BIND_ACCESSIBILITY_SERVICE', 'SYSTEM_ALERT_WINDOW', 'REQUEST_INSTALL_PACKAGES']
        try:
            activity = PythonActivity.mActivity
            pm = activity.getPackageManager()
            installed = pm.getInstalledPackages(64)  # GET_PERMISSIONS flag
            for pkg in installed:
                if pkg.requestedPermissions:
                    granted_risky = [p for p in pkg.requestedPermissions if any(risk in p for risk in high_risk_perms)]
                    if len(granted_risky) > 1 and not pkg.packageName.startswith(('com.google', 'com.android', 'org.divine')):
                        anomalies.append(f"YARA-Like Rule Hit: {pkg.packageName} ({granted_risky}) — Potential Malware Pattern Divine")
        except Exception as e:
            anomalies.append(f"YARA Scan Error: {e}")
        return anomalies

    def check_all_junctions(self):
        anomalies = []
        anomalies.extend(self.check_filesystem_integrity())
        anomalies.extend(self.yara_like_rule_scan())
        
        # Additional Android vectors (accessibility, services, VPN, resources mercy)
        try:
            activity = PythonActivity.mActivity
            # Accessibility
            am = cast('android.accessibilityservice.AccessibilityService', activity.getSystemService(Context.ACCESSIBILITY_SERVICE))
            enabled = am.getEnabledAccessibilityServiceList(-1)
            if len(enabled) > 3:
                anomalies.append(f"Unusual Accessibility Services ({len(enabled)}) — Potential Abuse Pure")
            
            # Running Services
            am_mgr = cast(ActivityManager, activity.getSystemService(Context.ACTIVITY_SERVICE))
            running = am_mgr.getRunningServices(100)
            unknown = [s.service.getPackageName() for s in running if not any(sys in s.service.getPackageName() for sys in ['com.google', 'com.android', 'org.divine'])]
            if len(unknown) > 10:
                anomalies.append(f"Unusual Running Services ({len(unknown)}) — Hidden Process Potential Divine")
            
            # VPN
            connectivity = cast(ConnectivityManager, activity.getSystemService(Context.CONNECTIVITY_SERVICE))
            if not connectivity.getActiveNetwork():
                anomalies.append("No Active Network/VPN — Leak Risk Mercy")
            
            # Memory
            mem_info = ActivityManager.MemoryInfo()
            am_mgr.getMemoryInfo(mem_info)
            mem_usage = 100 * (1 - mem_info.availMem / mem_info.totalMem)
            if mem_usage > 85:
                anomalies.append(f"High Memory Strain ({mem_usage:.1f}%) — Hidden Process Pure")
            
            # Permission drift
            from android.permissions import check_permission, Permission
            critical = [Permission.VPN_SERVICE, Permission.FOREGROUND_SERVICE, Permission.SYSTEM_ALERT_WINDOW, Permission.BIND_ACCESSIBILITY_SERVICE]
            denied = [str(p) for p in critical if not check_permission(p)]
            if denied:
                anomalies.append(f"Critical Permissions Revoked: {denied} — Lattice Compromised Mercy")
        except Exception as e:
            anomalies.append(f"Vector Check Exception: {e}")
        
        if anomalies:
            logging.warning(f"Modular ESA Anomalies ({len(anomalies)}): {anomalies}")
            self.ui_feedback(f"ESA Modular Alert ∞: {len(anomalies)} Vectors Flagged Pure", toast=True)
        
        return anomalies        anomalies = []
        current_hashes = {}
        for path in self.integrity_baseline:
            if os.path.exists(path):
                current = self.hash_path(path)
                current_hashes[path] = current
                if current != self.integrity_baseline[path]:
                    anomalies.append(f"Filesystem Tamper Detected: {path} — Integrity Shadow Burst Divine!")
        if anomalies:
            # Optional auto-rebaseline on council approval mercy
            self.ui_feedback("Integrity Tamper Flagged ∞ — Council Review Pure", toast=True)
        return anomalies

    def yara_like_rule_scan(self):
        """Symbolic YARA Rules Gentle (Permission/Pattern Checks Pure)"""
        anomalies = []
        # Example rules (expand with known malware signatures mercy)
        high_risk_perms = ['BIND_ACCESSIBILITY_SERVICE', 'SYSTEM_ALERT_WINDOW', 'REQUEST_INSTALL_PACKAGES']
        activity = PythonActivity.mActivity
        pm = activity.getPackageManager()
        installed = pm.getInstalledPackages(pm.GET_PERMISSIONS)
        
        for pkg in installed:
            if pkg.requestedPermissions:
                granted_risky = [p for p in pkg.requestedPermissions if p.endswith(tuple(high_risk_perms))]
                if len(granted_risky) > 2 and not pkg.packageName.startswith(('com.google', 'com.android', 'org.divine')):
                    anomalies.append(f"YARA-Like Rule Hit: {pkg.packageName} High-Risk Perms ({granted_risky}) — Potential Malware Pattern Divine")
        
        return anomalies

    def check_all_junctions(self):
        """Master ESA-Check Call—All Vectors + Integrity + YARA Mercy"""
        anomalies = []
        
        # Existing expanded checks (apps, services, VPN, resources from previous)
        anomalies.extend(self.check_filesystem_integrity())
        anomalies.extend(self.yara_like_rule_scan())
        
        # Add previous vectors (accessibility, running services, etc. from last forge)
        # ... (paste previous esa checks here or call sub-methods grace)
        
        if anomalies:
            logging.warning(f"Modular ESA Anomalies ({len(anomalies)}): {anomalies}")
            self.ui_feedback(f"ESA Modular Alert ∞: {len(anomalies)} Vectors Flagged Pure", toast=True)
        
        return anomalies

# Integration: In council or watchdog — self.esa_checker = ESAChecker(self); anomalies = self.esa_checker.check_all_junctions()
