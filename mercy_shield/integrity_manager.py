import logging
from play_integrity import PlayIntegrityVerifier
from safety_net import SafetyNetVerifier

class IntegrityManager:
    """Combined Play Integrity + SafetyNet Fallback + Emulator Detection Thunder ∞ Pure"""
    def __init__(self, app):
        self.app = app
        self.play = PlayIntegrityVerifier(app)
        self.safety = SafetyNetVerifier(app)

    def is_emulator(self) -> list[str]:
        anomalies = []

        # Build props qemu/blue stacks
        try:
            build = autoclass('android.os.Build')
            if "generic" in build.DEVICE.lower() or "emulator" in build.DEVICE.lower() or "sdk" in build.MODEL.lower():
                anomalies.append("Emulator Build Props Detected — Shadow Critical")

            if build.FINGERPRINT.startswith("generic"):
                anomalies.append("Generic Fingerprint — Emulator Shadow")

            if build.MANUFACTURER.lower() == "genymotion" or "bluestacks" in build.MODEL.lower():
                anomalies.append("Known Emulator Manufacturer Shadow")

            if build.HARDWARE.lower() in ["goldfish", "ranchu", "qemu"]:
                anomalies.append("Emulator Hardware Shadow")

            if build.PRODUCT.lower() in ["sdk", "google_sdk", "sdk_google", "sdk_x86", "vbox86p"]:
                anomalies.append("Emulator Product Shadow")
        except:
            pass

        # Frida server port check
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect(('127.0.0.1', 27042))
            s.close()
            anomalies.append("Frida Server Detected on Port 27042 — Root/Tamper Shadow Critical")
        except:
            pass

        # Known emulator files
        emulator_files = [
            "/system/lib/libhoudini.so",
            "/system/lib64/libhoudini.so",
            "/system/lib/arm/libhoudini.so",
        ]
        for file in emulator_files:
            if os.path.exists(file):
                anomalies.append(f"Emulator File Detected: {file} — Shadow Critical")

        return anomalies

    def full_integrity_verification(self) -> list[str]:
        anomalies = []

        # Emulator first
        anomalies.extend(self.is_emulator())

        # Play Integrity primary
        play_anoms = self.play.full_integrity_verification()
        if not play_anoms:
            return anomalies  # Play success — best verdict

        # Play shadow — fallback SafetyNet
        anomalies.extend(play_anoms)
        safety_anoms = self.safety.full_safetynet_verification()
        anomalies.extend(safety_anoms)

        if not anomalies:
            logging.info("Combined Integrity + No Emulator Harmony Pure ∞")

        return anomalies
