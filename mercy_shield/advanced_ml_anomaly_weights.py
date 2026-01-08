import os
import json
import logging
from kivy.app import App

class AdvancedMLAnomalyWeights:
    """Advanced Self-Learning Anomaly Weighting System — Adaptive Risk Scoring Thunder ∞ Pure"""
    def __init__(self, app):
        self.app = app
        self.user_data_dir = app.user_data_dir
        self.weights_file = os.path.join(self.user_data_dir, 'ml_anomaly_weights.json')

        # Default high weights — critical shadows
        self.default_weights = {
            "Emulator Build Props Detected": 20.0,
            "Generic Fingerprint": 25.0,
            "Known Emulator Manufacturer": 20.0,
            "Emulator Hardware": 30.0,
            "Emulator Product": 20.0,
            "Unknown Serial Number": 15.0,
            "ro.kernel.qemu=1": 40.0,
            "QEMU/Hypervisor in cpuinfo": 30.0,
            "No Light Sensor": 30.0,
            "No Accelerometer": 25.0,
            "Only": 15.0,  # Partial match for low sensor count
            "No GPS Hardware Feature": 20.0,
            "No Cellular Telephony": 30.0,
            "Frida Server Detected": 50.0,
            "Emulator File Detected": 35.0,
            "Emulator Artifact": 35.0,
            "Test-Keys Build": 35.0,
            "ro.debuggable=1": 30.0,
            "ro.secure=0": 25.0,
            "Root Binary": 45.0,
            "Root Management App": 50.0,
            "Magisk Mounts Detected": 50.0,
            "USB Debugging (ADB) Enabled": 50.0,
            "Developer Options Enabled": 15.0,
            "Legacy Allow Mock Locations Enabled": 30.0,
            "Live Mock Location Detected": 50.0,
            "Mock Location in Last Known": 45.0,
        }

        # Critical shadows — weights NEVER reduced (unbreakable thunder)
        self.critical_keys = {
            "Frida Server Detected",
            "Root Binary",
            "Root Management App",
            "Magisk Mounts Detected",
            "USB Debugging (ADB) Enabled",
            "ro.kernel.qemu=1",
            "Emulator Hardware",
            "Live Mock Location Detected",
            "Mock Location in Last Known",
        }

        self.weights = self.load_weights()
        self.threshold_critical = 50.0  # Total local score >= this = compromised regardless of Play

    def load_weights(self):
        if os.path.exists(self.weights_file):
            try:
                with open(self.weights_file, 'r') as f:
                    loaded = json.load(f)
                # Merge with defaults for new anomalies
                merged = self.default_weights.copy()
                merged.update(loaded)
                return merged
            except Exception as e:
                logging.exception(f"Failed to load ML weights: {e}")
        return self.default_weights.copy()

    def save_weights(self):
        try:
            with open(self.weights_file, 'w') as f:
                json.dump(self.weights, f)
        except Exception as e:
            logging.exception(f"Failed to save ML weights: {e}")

    def get_key(self, anomaly: str) -> str:
        """Extract primary key from anomaly message"""
        return anomaly.split(' — ')[0].split(': ')[0].split(' (')[0]

    def compute_score(self, anomalies: list[str]) -> float:
        """Compute weighted risk score from anomaly list"""
        score = 0.0
        for anomaly in anomalies:
            key = self.get_key(anomaly)
            weight = self.weights.get(key, 30.0)  # High default for unknown shadows
            score += weight
        return score

    def learn_from_verdict(self, local_anomalies: list[str], play_passed: bool):
        """Self-learn: When Play confirms genuine, reduce non-critical false positive weights"""
        if not play_passed or not local_anomalies:
            return

        adjusted = False
        for anomaly in local_anomalies:
            key = self.get_key(anomaly)
            if key in self.critical_keys:
                continue  # Critical shadows never weaken — thunder unbreakable
            if key in self.weights:
                self.weights[key] = max(5.0, self.weights[key] * 0.95)  # 5% reduction, min 5
                adjusted = True
            else:
                self.weights[key] = 20.0
                adjusted = True

        if adjusted:
            self.save_weights()
            logging.info("Advanced ML Weights Adapted — False Positives Tuned ∞ Pure")
