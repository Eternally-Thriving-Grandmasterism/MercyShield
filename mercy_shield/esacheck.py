import logging
import os
import hashlib
from jnius import autoclass, cast
from kivy.clock import Clock

PythonActivity = autoclass('org.kivy.android.PythonActivity')
Context = autoclass('android.content.Context')
ActivityManager = autoclass('android.app.ActivityManager')
ConnectivityManager = autoclass('android.net.ConnectivityManager')

class ESAChecker:
    """
    Modular ESA-Checker Pinnacle ∞ Pure — Local Vectors + Integrity + YARA Symbolic
    - Separate class for clean imports (from mercy_shield.esacheck import ESAChecker mercy)
    - Filesystem integrity hashes (key dirs/files tamper detect divine)
    - YARA-like rule symbolic (permission/pattern checks gentle)
    - All Android user-level vectors monitored proactive eternal
    """

    def __init__(self, app_instance=None):
        self.app = app_instance
        self.integrity_baseline = {}  # {path: hash} — computed first run mercy
        self.baseline_file = '/sdcard/MercyShield/integrity_baseline.txt'  # Persistent gentle
        self.load_baseline()

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

    def load_baseline(self):
        """Load or create integrity baseline divine"""
        if os.path.exists(self.baseline_file):
            with open(self.baseline_file, 'r') as f:
                for line in f:
                    path, hash_val = line.strip().split(':')
                    self.integrity_baseline[path] = hash_val
        else:
            self.compute_baseline()  # First run mercy

    def compute_baseline(self):
        """Hash key app directories/files gentle (tamper baseline pure)"""
        key_paths = [
            '/data/data/org.divine.mercyshield/',  # App data (if accessible mercy)
            '/sdcard/MercyShield/',                # Our logs/storage
            PythonActivity.mActivity.getFilesDir().getAbsolutePath()  # Internal files divine
        ]
        for path in key_paths:
            if os.path.exists(path):
                hash_val = self.hash_path(path)
                self.integrity_baseline[path] = hash_val
        self.save_baseline()

    def save_baseline(self):
        os.makedirs(os.path.dirname(self.baseline_file), exist_ok=True)
        with open(self.baseline_file, 'w') as f:
            for path, hash_val in self.integrity_baseline.items():
                f.write(f"{path}:{hash_val}\n")

    def hash_path(self, path):
        """SHA256 hash directory/files recursive mercy"""
        sha256 = hashlib.sha256()
        if os.path.isfile(path):
            with open(path, 'rb') as f:
                for block in iter(lambda: f.read(4096), b""):
                    sha256.update(block)
        else:
            for root, _, files in os.walk(path):
                for file in sorted(files):  # Deterministic gentle
                    with open(os.path.join(root, file), 'rb') as f:
                        for block in iter(lambda: f.read(4096), b""):
                            sha256.update(block)
        return sha256.hexdigest()

    def check_filesystem_integrity(self):
        """Tamper Detection Thunder—Compare current hashes"""
        anomalies = []
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
