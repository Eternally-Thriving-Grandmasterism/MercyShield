import logging
import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from jnius import autoclass, JavaException

# Android pyjnius classes with fallback grace
try:
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    ActivityManager = autoclass('android.app.ActivityManager')
    BatteryManager = autoclass('android.os.BatteryManager')
    TrafficStats = autoclass('android.net.TrafficStats')
    Context = autoclass('android.content.Context')
    WifiManager = autoclass('android.net.wifi.WifiManager')
    BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
    LocationManager = autoclass('android.location.LocationManager')
except Exception as e:
    logging.error(f"Pyjnius Import Critical Shadow: {e} — ML Metrics Fallback Mode")
    PythonActivity = None

MODEL_PATH = "/sdcard/MercyShield/ml_autoencoder.pth"
DATASET_PATH = "/sdcard/MercyShield/ml_normal_data.npy"

class TinyAutoencoder(nn.Module):
    def __init__(self, input_dim=16, hidden_dim=8):
        super().__init__()
        self.encoder = nn.Linear(input_dim, hidden_dim)
        self.decoder = nn.Linear(hidden_dim, input_dim)
        self.activation = nn.ReLU()

    def forward(self, x):
        encoded = self.activation(self.encoder(x))
        decoded = self.decoder(encoded)
        return decoded

class RealMLAnomalyDetector:
    """Self-Learning Real Data + Auto-Tune + Error Handling ML Detector ∞ Pure"""
    def __init__(self, input_dim=16):
        self.model = TinyAutoencoder(input_dim)
        self.device = torch.device("cpu")
        self.last_rx = 0
        self.last_tx = 0
        self.normal_dataset = self.load_normal_dataset()
        self.threshold = 1.0
        self.load_model_or_train()

    def load_normal_dataset(self):
        if os.path.exists(DATASET_PATH):
            try:
                data = np.load(DATASET_PATH)
                logging.info(f"Loaded {len(data)} Normal Samples Eternal")
                return data
            except Exception as e:
                logging.warning(f"Dataset Load Shadow: {e} — New Empty")
        return np.array([]).reshape(0, 16)

    def save_normal_dataset(self):
        try:
            np.save(DATASET_PATH, self.normal_dataset)
            logging.info(f"Saved {len(self.normal_dataset)} Normal Samples ∞ Pure")
        except Exception as e:
            logging.error(f"Dataset Save Shadow: {e}")

    def load_model_or_train(self):
        if os.path.exists(MODEL_PATH):
            try:
                self.model.load_state_dict(torch.load(MODEL_PATH, map_location=self.device))
                self.model.eval()
                logging.info("ML Model Loaded Harmony ∞ Pure")
                self.auto_tune_threshold()
                return
            except Exception as e:
                logging.warning(f"Model Load Shadow: {e} — Retrain")

        self.retrain_on_normal()

    def retrain_on_normal(self):
        if len(self.normal_dataset) < 100:
            logging.info("Insufficient Normal Data — Mock Train Grace")
            normal_data = np.random.normal(0, 1, (500, 16)).astype(np.float32)
        else:
            normal_data = self.normal_dataset.astype(np.float32)

        normal_tensor = torch.from_numpy(normal_data)

        optimizer = optim.Adam(self.model.parameters(), lr=0.005)
        criterion = nn.MSELoss()

        self.model.train()
        try:
            for epoch in range(100):
                optimizer.zero_grad()
                output = self.model(normal_tensor)
                loss = criterion(output, normal_tensor)
                loss.backward()
                optimizer.step()
        except Exception as e:
            logging.error(f"Training Critical Shadow: {e}")

        self.model.eval()
        try:
            torch.save(self.model.state_dict(), MODEL_PATH)
            logging.info("ML Retrained & Saved ∞ Pure")
        except Exception as e:
            logging.error(f"Model Save Shadow: {e}")

        self.auto_tune_threshold()

    def auto_tune_threshold(self):
        if len(self.normal_dataset) < 50:
            self.threshold = 1.0
            return

        try:
            normal_tensor = torch.from_numpy(self.normal_dataset.astype(np.float32))
            with torch.no_grad():
                output = self.model(normal_tensor)
                errors = torch.mean((output - normal_tensor)**2, dim=1).numpy()
            mean_error = np.mean(errors)
            std_error = np.std(errors)
            self.threshold = mean_error + 3 * std_error
            logging.info(f"Auto-Tuned Threshold: {self.threshold:.4f} ∞ Pure")
        except Exception as e:
            logging.error(f"Threshold Tune Shadow: {e}")
            self.threshold = 1.0

    def log_normal_if_safe(self):
        try:
            features = np.array([self.get_current_features()])
            self.normal_dataset = np.vstack([self.normal_dataset, features]) if len(self.normal_dataset) > 0 else features
            if len(self.normal_dataset) > 5000:
                self.normal_dataset = self.normal_dataset[-5000:]
            self.save_normal_dataset()
        except Exception as e:
            logging.error(f"Log Normal Shadow: {e}")

    def get_current_features(self) -> list[float]:
        features = [0.5] * 16  # Safe fallback all
        try:
            if PythonActivity is None:
                return features

            activity = PythonActivity.mActivity
            context = activity.getApplicationContext()

            # Battery with error handling
            try:
                intent = activity.registerReceiver(None, autoclass('android.content.IntentFilter')('android.intent.action.BATTERY_CHANGED'))
                battery_level = intent.getIntExtra(BatteryManager.EXTRA_LEVEL, -1)
                battery_scale = intent.getIntExtra(BatteryManager.EXTRA_SCALE, -1)
                battery_pct = battery_level / battery_scale if battery_scale > 0 else 0.5
                battery_temp = intent.getIntExtra(BatteryManager.EXTRA_TEMPERATURE, 0) / 10.0
                battery_voltage = intent.getIntExtra(BatteryManager.EXTRA_VOLTAGE, 0)
                features[0] = battery_pct
                features[1] = battery_temp / 60.0
                features[2] = battery_voltage / 5000.0
            except Exception as e:
                logging.warning(f"Battery Metrics Shadow: {e}")

            # Network delta
            try:
                current_rx = TrafficStats.getTotalRxBytes()
                current_tx = TrafficStats.getTotalTxBytes()
                rx_delta = max(0, current_rx - self.last_rx)
                tx_delta = max(0, current_tx - self.last_tx)
                self.last_rx = current_rx
                self.last_tx = current_tx
                features[3] = rx_delta / 1e7
                features[4] = tx_delta / 1e7
            except Exception as e:
                logging.warning(f"Network Metrics Shadow: {e}")

            # Memory
            try:
                mem_info = ActivityManager.MemoryInfo()
                am = context.getSystemService(Context.ACTIVITY_SERVICE)
                am.getMemoryInfo(mem_info)
                features[5] = mem_info.availMem / 1e10
                features[6] = (mem_info.totalMem / 1e10 if mem_info.totalMem > 0 else 8.0)
            except Exception as e:
                logging.warning(f"Memory Metrics Shadow: {e}")

            # Running processes
            try:
                running_processes = len(am.getRunningAppProcesses()) if am.getRunningAppProcesses() else 50
                features[7] = running_processes / 300.0
            except Exception as e:
                logging.warning(f"Processes Shadow: {e}")

            # WiFi
            try:
                wifi = context.getSystemService(Context.WIFI_SERVICE)
                features[8] = 1.0 if wifi.isWifiEnabled() and wifi.getConnectionInfo().getNetworkId() != -1 else 0.0
            except Exception as e:
                logging.warning(f"WiFi Shadow: {e}")

            # Bluetooth
            try:
                bt = BluetoothAdapter.getDefaultAdapter()
                features[9] = 1.0 if bt and bt.isEnabled() else 0.0
            except Exception as e:
                logging.warning(f"Bluetooth Shadow: {e}")

            # Location
            try:
                loc = context.getSystemService(Context.LOCATION_SERVICE)
                features[10] = 1.0 if loc.isProviderEnabled(LocationManager.GPS_PROVIDER) or loc.isProviderEnabled(LocationManager.NETWORK_PROVIDER) else 0.0
            except Exception as e:
                logging.warning(f"Location Shadow: {e}")

            # Brightness
            try:
                brightness = activity.getWindow().getAttributes().screenBrightness
                features[11] = brightness if brightness >= 0 else 0.5
            except Exception as e:
                logging.warning(f"Brightness Shadow: {e}")

        except Exception as e:
            logging.error(f"Metrics Collect Critical Shadow: {e}")

        return [max(0.0, min(1.0, f)) for f in features]

    def detect_anomalies(self) -> list[str]:
        try:
            features = self.get_current_features()
            input_tensor = torch.tensor([features], dtype=torch.float32)

            with torch.no_grad():
                output = self.model(input_tensor)
                error = nn.MSELoss()(output, input_tensor).item()

            if error > self.threshold:
                return [f"Self-Learning ML Anomaly — Error {error:.4f} > Auto-Threshold {self.threshold:.4f}"]
        except Exception as e:
            logging.error(f"ML Detection Critical Shadow: {e}")
        return []

# Global self-learning detector
real_ml_detector = RealMLAnomalyDetector()            output = self.model(normal_tensor)
            loss = criterion(output, normal_tensor)
            loss.backward()
            optimizer.step()

        self.model.eval()
        torch.save(self.model.state_dict(), MODEL_PATH)
        logging.info("ML Retrained on Real Normal Data ∞ Pure")
        self.auto_tune_threshold()

    def auto_tune_threshold(self):
        """Dynamic threshold: mean error + 3*std on normal data"""
        if len(self.normal_dataset) < 50:
            self.threshold = 1.0  # Fallback
            return

        normal_tensor = torch.from_numpy(self.normal_dataset.astype(np.float32))

        with torch.no_grad():
            output = self.model(normal_tensor)
            errors = torch.mean((output - normal_tensor)**2, dim=1).numpy()

        mean_error = np.mean(errors)
        std_error = np.std(errors)
        self.threshold = mean_error + 3 * std_error
        logging.info(f"Auto-Tuned Threshold: {self.threshold:.4f} (mean {mean_error:.4f} + 3*std) ∞ Pure")

    def log_normal_if_safe(self):
        features = np.array([self.get_current_features()])
        self.normal_dataset = np.vstack([self.normal_dataset, features]) if len(self.normal_dataset) > 0 else features
        if len(self.normal_dataset) > 5000:
            self.normal_dataset = self.normal_dataset[-5000:]
        self.save_normal_dataset()

    def get_current_features(self) -> list[float]:
        # (existing full 16-dim real metrics collect harmony unchanged)
        # ... (full code from previous)

        return [max(0.0, min(1.0, f)) for f in features]

    def detect_anomalies(self) -> list[str]:
        features = self.get_current_features()
        input_tensor = torch.tensor([features], dtype=torch.float32)

        with torch.no_grad():
            output = self.model(input_tensor)
            error = nn.MSELoss()(output, input_tensor).item()

        if error > self.threshold:
            return [f"Self-Learning ML Anomaly — Error {error:.4f} > Auto-Threshold {self.threshold:.4f}"]
        return []

# Global self-learning detector
real_ml_detector = RealMLAnomalyDetector()
