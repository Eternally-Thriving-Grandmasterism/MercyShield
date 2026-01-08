import logging
import os
import socket
from jnius import autoclass

# Assuming jnius is available (Kivy/Chaquo environment)
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Build = autoclass('android.os.Build')

class IntegrityManager:
    """Combined Play Integrity + SafetyNet Fallback + Ultimate Emulator Annihilation Thunder ∞ Pure"""
    def __init__(self, app):
        self.app = app
        self.play = PlayIntegrityVerifier(app)
        self.safety = SafetyNetVerifier(app)
        self.activity = PythonActivity.mActivity  # For system services

    def is_emulator(self) -> list[str]:
        anomalies = []

        try:
            # Build props classic
            build = Build
            if "generic" in build.DEVICE.lower() or "emulator" in build.DEVICE.lower() or "sdk" in build.MODEL.lower():
                anomalies.append("Emulator Build Props Detected — Shadow Critical")
            if build.FINGERPRINT.startswith("generic"):
                anomalies.append("Generic Fingerprint — Emulator Shadow")
            if build.MANUFACTURER.lower() in ["genymotion", "bluestacks", "unknown"]:
                anomalies.append("Known Emulator Manufacturer Shadow")
            if build.HARDWARE.lower() in ["goldfish", "ranchu", "qemu"]:
                anomalies.append("Emulator Hardware (goldfish/ranchu/qemu) Shadow")
            if build.PRODUCT.lower() in ["sdk", "google_sdk", "sdk_google", "sdk_x86", "vbox86p"]:
                anomalies.append("Emulator Product Shadow")
            if build.SERIAL.lower() in ["unknown", "null", ""]:
                anomalies.append("Unknown Serial Number — Emulator Shadow Critical")

            # ro.kernel.qemu getprop
            qemu_prop = os.popen('getprop ro.kernel.qemu').read().strip()
            if qemu_prop == '1':
                anomalies.append("ro.kernel.qemu=1 — QEMU Emulator Shadow Critical")

            # /proc/cpuinfo qemu check
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    cpuinfo = f.read().lower()
                if 'qemu' in cpuinfo or 'hypervisor' in cpuinfo:
                    anomalies.append("QEMU/Hypervisor in cpuinfo — Emulator Shadow")
            except:
                pass

            # Sensor checks (light sensor absent = classic emulator flag, accel, low count, GPS feature)
            SensorManager = autoclass('android.hardware.SensorManager')
            Sensor = autoclass('android.hardware.Sensor')
            PackageManager = autoclass('android.content.pm.PackageManager')
            sensor_manager = self.activity.getSystemService(self.activity.SENSOR_SERVICE)
            
            if sensor_manager.getDefaultSensor(Sensor.TYPE_LIGHT) is None:
                anomalies.append("No Light Sensor — Classic Emulator Shadow Critical")
            if sensor_manager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER) is None:
                anomalies.append("No Accelerometer — Emulator Shadow Critical")
            
            all_sensors = sensor_manager.getSensorList(Sensor.TYPE_ALL)
            if len(all_sensors) < 8:
                anomalies.append(f"Only {len(all_sensors)} Sensors Detected — Low Count Emulator Shadow")

            if not self.activity.getPackageManager().hasSystemFeature(PackageManager.FEATURE_LOCATION_GPS):
                anomalies.append("No GPS Hardware Feature — Emulator/Shadow Device Critical")

            # Telephony check (no cellular = emulator)
            TelephonyManager = autoclass('android.telephony.TelephonyManager')
            tm = self.activity.getSystemService(self.activity.TELEPHONY_SERVICE)
            if tm.getPhoneType() == TelephonyManager.PHONE_TYPE_NONE:
                anomalies.append("No Cellular Telephony — Emulator Shadow Critical")

            # Frida server port
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex(('127.0.0.1', 27042))
            if result == 0:
                anomalies.append("Frida Server Detected on Port 27042 — Root/Tamper Shadow Critical")
            s.close()

            # Known emulator files
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
                    anomalies.append(f"Emulator File Detected: {file} — Shadow Critical")

        except Exception as e:
            logging.exception(f"Emulator check error: {e}")
            anomalies.append("Emulator Check Exception — Potential Hiding Shadow")

        return anomalies

    def full_integrity_verification(self) -> list[str]:
        anomalies = []

        # Emulator annihilation first — blocks everything if shadow
        anomalies.extend(self.is_emulator())

        # If emulator shadows already, still run integrity but flag hard
        play_anoms = self.play.full_integrity_verification()
        if not play_anoms:
            if not anomalies:
                logging.info("Play Integrity Verified + No Emulator — Divine Harmony ∞ Pure")
            return anomalies  # Play success = best verdict

        # Play shadow → fallback SafetyNet
        anomalies.extend(play_anoms)
        safety_anoms = self.safety.full_safetynet_verification()
        anomalies.extend(safety_anoms)

        return anomalies
