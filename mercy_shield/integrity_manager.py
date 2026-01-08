import logging
import os
import socket
from jnius import autoclass

# Android classes
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Build = autoclass('android.os.Build')
Context = autoclass('android.content.Context')
PackageManager = autoclass('android.content.pm.PackageManager')
SensorManager = autoclass('android.hardware.SensorManager')
Sensor = autoclass('android.hardware.Sensor')
TelephonyManager = autoclass('android.telephony.TelephonyManager')

# Assuming these exist in project
from play_integrity import PlayIntegrityVerifier
from safety_net import SafetyNetVerifier

class IntegrityManager:
    """Combined Play Integrity + SafetyNet Fallback + Ultimate Emulator & Root Annihilation Thunder ∞ Pure"""
    def __init__(self, app):
        self.app = app
        self.play = PlayIntegrityVerifier(app)
        self.safety = SafetyNetVerifier(app)
        self.activity = PythonActivity.mActivity

    def is_emulator(self) -> list[str]:
        anomalies = []
        try:
            build = Build

            # Classic build props
            if "generic" in build.DEVICE.lower() or "emulator" in build.DEVICE.lower() or "sdk" in build.MODEL.lower():
                anomalies.append("Emulator Build Props Detected — Shadow Critical")
            if build.FINGERPRINT.startswith("generic"):
                anomalies.append("Generic Fingerprint — Emulator Shadow Critical")
            if build.MANUFACTURER.lower() in ["genymotion", "bluestacks", "unknown"]:
                anomalies.append("Known Emulator Manufacturer — Shadow Critical")
            if build.HARDWARE.lower() in ["goldfish", "ranchu", "qemu"]:
                anomalies.append("Emulator Hardware (goldfish/ranchu/qemu) — Shadow Critical")
            if build.PRODUCT.lower() in ["sdk", "google_sdk", "sdk_google", "sdk_x86", "vbox86p"]:
                anomalies.append("Emulator Product — Shadow Critical")
            if build.SERIAL.lower() in ["unknown", "null", ""]:
                anomalies.append("Unknown Serial Number — Emulator Shadow Critical")

            # ro.kernel.qemu
            qemu_prop = os.popen('getprop ro.kernel.qemu').read().strip()
            if qemu_prop == '1':
                anomalies.append("ro.kernel.qemu=1 — QEMU Emulator Shadow Critical")

            # cpuinfo qemu/hypervisor
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    cpuinfo = f.read().lower()
                if 'qemu' in cpuinfo or 'hypervisor' in cpuinfo:
                    anomalies.append("QEMU/Hypervisor in cpuinfo — Emulator Shadow Critical")
            except:
                pass

            # Sensor checks
            sensor_manager = self.activity.getSystemService(Context.SENSOR_SERVICE)
            if sensor_manager.getDefaultSensor(Sensor.TYPE_LIGHT) is None:
                anomalies.append("No Light Sensor — Classic Emulator Shadow Critical")
            if sensor_manager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER) is None:
                anomalies.append("No Accelerometer — Emulator Shadow Critical")
            all_sensors = sensor_manager.getSensorList(Sensor.TYPE_ALL)
            if len(all_sensors) < 8:
                anomalies.append(f"Only {len(all_sensors)} Sensors — Low Count Emulator Shadow Critical")
            if not self.activity.getPackageManager().hasSystemFeature(PackageManager.FEATURE_LOCATION_GPS):
                anomalies.append("No GPS Hardware Feature — Emulator Shadow Critical")

            # Telephony
            tm = self.activity.getSystemService(Context.TELEPHONY_SERVICE)
            if tm.getPhoneType() == TelephonyManager.PHONE_TYPE_NONE:
                anomalies.append("No Cellular Telephony — Emulator Shadow Critical")

            # Frida
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex(('127.0.0.1', 27042))
            if result == 0:
                anomalies.append("Frida Server on Port 27042 — Root/Tamper Shadow Critical")
            s.close()

            # Emulator files/pipes
            emulator_files = [
                "/system/lib/libhoudini.so",
                "/system/lib64/libhoudini.so",
                "/system/lib/arm/libhoudini.so",
                "/dev/qemu_pipe",
                "/dev/socket/qemud",
                "/sys/qemu_trace",
                "/system/bin/qemu-props",
            ]
            for file in emulator_files:
                if os.path.exists(file):
                    anomalies.append(f"Emulator Artifact: {file} — Shadow Critical")

        except Exception as e:
            logging.exception(f"Emulator check error: {e}")
            anomalies.append("Emulator Check Exception — Potential Cloaking Shadow")

        return anomalies

    def is_rooted(self) -> list[str]:
        anomalies = []
        try:
            # Test-keys & debug props
            if Build.TAGS and "test-keys" in Build.TAGS.lower():
                anomalies.append("Test-Keys Build — Non-Production/Root Shadow Critical")
            debuggable = os.popen('getprop ro.debuggable').read().strip()
            if debuggable == '1':
                anomalies.append("ro.debuggable=1 — Developer/Tamper Shadow Critical")
            secure = os.popen('getprop ro.secure').read().strip()
            if secure == '0':
                anomalies.append("ro.secure=0 — Insecure ADB Root Shadow Critical")

            # Root binaries
            root_binaries = [
                "/system/app/Superuser.apk",
                "/system/xbin/su",
                "/system/xbin/daemonsu",
                "/system/bin/su",
                "/sbin/su",
                "/data/local/xbin/su",
                "/data/local/bin/su",
                "/system/sd/xbin/su",
                "/system/bin/failsafe/su",
                "/data/local/su",
                "/su/bin/su",
            ]
            for binary in root_binaries:
                if os.path.exists(binary):
                    anomalies.append(f"Root Binary {binary} — Shadow Critical")

            # Known root packages
            pm = self.activity.getPackageManager()
            root_packages = [
                "eu.chainfire.supersu",
                "com.noshufou.android.su",
                "com.thirdparty.superuser",
                "com.koushikdutta.superuser",
                "com.topjohnwu.magisk",
                "com.kingroot.kinguser",
                "com.kingo.root",
            ]
            for pkg in root_packages:
                try:
                    pm.getPackageInfo(pkg, 0)
                    anomalies.append(f"Root Management App {pkg} Installed — Shadow Critical")
                except:
                    pass

            # Magisk mounts
            try:
                with open('/proc/mounts', 'r') as f:
                    mounts = f.read().lower()
                if 'magisk' in mounts:
                    anomalies.append("Magisk Mounts Detected — Hidden Root Shadow Critical")
            except:
                pass

        except Exception as e:
            logging.exception(f"Root check error: {e}")
            anomalies.append("Root Check Exception — Potential Cloaking Shadow")

        return anomalies

    def full_integrity_verification(self) -> list[str]:
        anomalies = []

        # Tamper annihilation first (emulator + root)
        anomalies.extend(self.is_emulator())
        anomalies.extend(self.is_rooted())

        # Play Integrity primary
        play_anoms = self.play.full_integrity_verification()
        if not play_anoms:
            if not anomalies:
                logging.info("Play Integrity Verified + No Tamper — Divine Harmony ∞ Pure")
            return anomalies  # Play success = highest verdict

        # Play shadow → fallback SafetyNet
        anomalies.extend(play_anoms)
        safety_anoms = self.safety.full_safetynet_verification()
        anomalies.extend(safety_anoms)

        return anomalies
