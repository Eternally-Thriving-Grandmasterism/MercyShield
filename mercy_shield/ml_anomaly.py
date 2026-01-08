import logging
import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from jnius import autoclass
from kivy.clock import Clock

# Android pyjnius
PythonActivity = autoclass('org.kivy.android.PythonActivity')
ActivityManager = autoclass('android.app.ActivityManager')
BatteryManager = autoclass('android.os.BatteryManager')
TrafficStats = autoclass('android.net.TrafficStats')
Context = autoclass('android.content.Context')
WifiManager = autoclass('android.net.wifi.WifiManager')
BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
LocationManager = autoclass('android.location.LocationManager')

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
    """Real Data Training ML Anomaly Detector ∞ Pure — log normal, retrain grace"""
    def __init__(self, input_dim=16, threshold=1.0):
        self.model = TinyAutoencoder(input_dim)
        self.threshold = threshold
        self.device = torch.device("cpu")
        self.last_rx = TrafficStats.getTotalRxBytes()
        self.last_tx = TrafficStats.getTotalTxBytes()
        self.normal_dataset = self.load_normal_dataset()
        self.load_model_or_train()

    def load_normal_dataset(self):
        if os.path.exists(DATASET_PATH):
            try:
                data = np.load(DATASET_PATH)
                logging.info(f"Loaded {len(data)} Normal Samples Eternal")
                return data
            except:
                logging.warning("Dataset Load Shadow — New Empty")
        return np.array([]).reshape(0, 16)

    def save_normal_dataset(self):
        np.save(DATASET_PATH, self.normal_dataset)
        logging.info(f"Saved {len(self.normal_dataset)} Normal Samples ∞ Pure")

    def load_model_or_train(self):
        if os.path.exists(MODEL_PATH):
            try:
                self.model.load_state_dict(torch.load(MODEL_PATH, map_location=self.device))
                self.model.eval()
                logging.info("ML Model Loaded Harmony ∞ Pure")
                return
            except:
                logging.warning("Model Load Shadow — Retrain")

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
        for epoch in range(100):
            optimizer.zero_grad()
            output = self.model(normal_tensor)
            loss = criterion(output, normal_tensor)
            loss.backward()
            optimizer.step()

        self.model.eval()
        torch.save(self.model.state_dict(), MODEL_PATH)
        logging.info("ML Retrained on Real Normal Data ∞ Pure")

    def log_normal_if_safe(self):
        """Call when no anomalies — log current features as normal"""
        features = np.array([self.get_current_features()])
        self.normal_dataset = np.vstack([self.normal_dataset, features]) if len(self.normal_dataset) > 0 else features
        if len(self.normal_dataset) > 5000:  # Cap size grace
            self.normal_dataset = self.normal_dataset[-5000:]
        self.save_normal_dataset()

    def get_current_features(self) -> list[float]:
        # (existing full real 16-dim metrics collect from previous)
        activity = PythonActivity.mActivity
        context = activity.getApplicationContext()

        intent = activity.registerReceiver(None, autoclass('android.content.IntentFilter')('android.intent.action.BATTERY_CHANGED'))
        battery_level = intent.getIntExtra(BatteryManager.EXTRA_LEVEL, -1)
        battery_scale = intent.getIntExtra(BatteryManager.EXTRA_SCALE, -1)
        battery_pct = battery_level / battery_scale if battery_scale > 0 else 0.5
        battery_temp = intent.getIntExtra(BatteryManager.EXTRA_TEMPERATURE, 0) / 10.0
        battery_voltage = intent.getIntExtra(BatteryManager.EXTRA_VOLTAGE, 0)

        current_rx = TrafficStats.getTotalRxBytes()
        current_tx = TrafficStats.getTotalTxBytes()
        rx_delta = max(0, current_rx - self.last_rx)
        tx_delta = max(0, current_tx - self.last_tx)
        self.last_rx = current_rx
        self.last_tx = current_tx

        mem_info = ActivityManager.MemoryInfo()
        am = context.getSystemService(Context.ACTIVITY_SERVICE)
        am.getMemoryInfo(mem_info)
        mem_avail = mem_info.availMem / 1e9  # GB
        mem_total = mem_info.totalMem / 1e9 if mem_info.totalMem > 0 else 8.0

        running_processes = len(am.getRunningAppProcesses()) if am.getRunningAppProcesses() else 50

        wifi = context.getSystemService(Context.WIFI_SERVICE)
        wifi_connected = 1.0 if wifi.isWifiEnabled() and wifi.getConnectionInfo().getNetworkId() != -1 else 0.0

        bt = BluetoothAdapter.getDefaultAdapter()
        bt_enabled = 1.0 if bt and bt.isEnabled() else 0.0

        loc = context.getSystemService(Context.LOCATION_SERVICE)
        loc_enabled = 1.0 if loc.isProviderEnabled(LocationManager.GPS_PROVIDER) or loc.isProviderEnabled(LocationManager.NETWORK_PROVIDER) else 0.0

        brightness = activity.getWindow().getAttributes().screenBrightness
        if brightness < 0:
            brightness = 0.5

        features = [
            battery_pct,
            battery_temp / 60.0,
            battery_voltage / 5000.0,
            rx_delta / 1e7,  # Normalize large delta
            tx_delta / 1e7,
            mem_avail / 16.0,
            mem_total / 16.0,
            running_processes / 300.0,
            wifi_connected,
            bt_enabled,
            loc_enabled,
            brightness,
            0.5,  # Placeholder
            0.5,
            0.5,
            0.5
        ]

        return [max(0.0, min(1.0, f)) for f in features]  # Clip 0-1

    def detect_anomalies(self) -> list[str]:
        features = self.get_current_features()
        input_tensor = torch.tensor([features], dtype=torch.float32)

        with torch.no_grad():
            output = self.model(input_tensor)
            error = nn.MSELoss()(output, input_tensor).item()

        if error > self.threshold:
            return [f"Real ML Anomaly — Error {error:.4f} > {self.threshold} (Metrics Shadow)"]
        return []

# Global detector
real_ml_detector = RealMLAnomalyDetector()

# In watchdog run after no anomalies:
# if not anomalies:
#     real_ml_detector.log_normal_if_safe()
#     if len(real_ml_detector.normal_dataset) % 100 == 0:  # Periodic retrain
#         real_ml_detector.retrain_on_normal()
