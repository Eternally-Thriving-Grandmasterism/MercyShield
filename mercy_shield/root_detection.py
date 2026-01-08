import logging
import os
import subprocess
from jnius import autoclass, JavaException

# Android pyjnius classes
try:
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Context = autoclass('android.content.Context')
    PackageManager = autoclass('android.content.pm.PackageManager')
except Exception as e:
    logging.error(f"Root Pyjnius Shadow: {e}")
    PythonActivity = None

# Known root binaries paths
ROOT_BIN_PATHS = [
    "/system/app/Superuser.apk",
    "/sbin/su",
    "/system/bin/su",
    "/system/xbin/su",
    "/data/local/xbin/su",
    "/data/local/bin/su",
    "/system/sd/xbin/su",
    "/system/bin/failsafe/su",
    "/data/local/su",
    "/su/bin/su",
]

# Known root packages
ROOT_PACKAGES = [
    "com.noshufou.android.su",
    "com.thirdparty.superuser",
    "eu.chainfire.supersu",
    "com.koushikdutta.superuser",
    "com.zachspong.temprootremovejb",
    "com.ramdroid.appquarantine",
    "com.topjohnwu.magisk",  # Magisk
]

class RootDetector:
    """Real Root/Jailbreak Detection Thunder ∞ Pure — Multi-method Android root check"""
    def __init__(self, app):
        self.app = app
        self.activity = PythonActivity.mActivity if PythonActivity else None
        self.package_manager = self.activity.getPackageManager() if self.activity else None

    def check_root_binaries(self) -> list[str]:
        anomalies = []
        for path in ROOT_BIN_PATHS:
            if os.path.exists(path):
                anomalies.append(f"Root Binary Detected: {path} — Device Rooted Shadow Critical")
        return anomalies

    def check_test_keys(self) -> list[str]:
        try:
            build_tags = autoclass('android.os.Build').TAGS
            if build_tags and "test-keys" in build_tags:
                return ["Test-Keys Build Tag — Rooted Device Shadow Critical"]
        except:
            pass
        return []

    def check_root_packages(self) -> list[str]:
        anomalies = []
        if not self.package_manager:
            return ["Root Package Check Shadow — API Unavailable"]

        for package in ROOT_PACKAGES:
            try:
                self.package_manager.getPackageInfo(package, 0)
                anomalies.append(f"Root Package Detected: {package} — Device Rooted Shadow Critical")
            except JavaException:
                continue
        return anomalies

    def check_su_execute(self) -> list[str]:
        try:
            process = subprocess.Popen(["su"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.communicate(timeout=5)
            if process.returncode == 0:
                return ["SU Execute Success — Device Rooted Shadow Critical"]
        except:
            pass
        return []

    def check_busybox(self) -> list[str]:
        try:
            process = subprocess.Popen(["busybox"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.communicate(timeout=5)
            if process.returncode == 0:
                return ["BusyBox Detected — Root Tool Shadow"]
        except:
            pass
        return []

    def full_root_verification(self) -> list[str]:
        anomalies = []

        anomalies.extend(self.check_root_binaries())
        anomalies.extend(self.check_test_keys())
        anomalies.extend(self.check_root_packages())
        anomalies.extend(self.check_su_execute())
        anomalies.extend(self.check_busybox())

        if anomalies:
            logging.warning(f"Root Detected: {anomalies}")
        else:
            logging.info("No Root Detected — Device Harmony Pure ∞")

        return anomalies
