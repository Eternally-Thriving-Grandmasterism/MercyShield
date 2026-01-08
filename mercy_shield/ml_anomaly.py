import logging
import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from jnius import autoclass
from kivy.clock import Clock

# Android pyjnius classes
PythonActivity = autoclass('org.kivy.android.PythonActivity')
ActivityManager = autoclass('android.app.ActivityManager')
BatteryManager = autoclass('android.os.BatteryManager')
TrafficStats = autoclass('android.net.TrafficStats')
Context = autoclass('android.content.Context')
WifiManager = autoclass('android.net.wifi.WifiManager')
BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
LocationManager = autoclass('android.location.LocationManager')

MODEL_PATH = "/sdcard/MercyShield/ml_autoencoder.pth"

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
    """Real Feature Vector ML Anomaly Detector ∞ Pure — mobile metrics"""
    def __init__(self, input_dim=16, threshold=1.0):
        self.model = TinyAutoencoder(input_dim)
        self.threshold = threshold
        self.device = torch.device("cpu")
        self.last_rx = TrafficStats.getTotalRxBytes()
        self.last_tx = TrafficStats.getTotalTxBytes()
        self.load_model()

    def load_model(self):
        if os.path.exists(MODEL_PATH):
            try:
                self.model.load_state_dict(torch.load(MODEL_PATH, map_location=self.device))
                self.model.eval()
                logging.info("Real ML Autoencoder Loaded Harmony ∞ Pure")
            except Exception as e:
                logging.warning(f"Model Load Shadow: {e} — Train New")
                self.train_mock_normal()
        else:
            self.train_mock_normal()

    def train_mock_normal(self):
        # Mock normal real-like vectors (evolve to log real normal over time)
        normal_data = np.random.normal(0, 1, (500, 16)).astype(np.float32)  # Normalized
        normal_tensor = torch.from_numpy(normal_data)

        optimizer = optim.Adam(self.model.parameters(), lr=0.01)
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
        logging.info("Real ML Autoencoder Trained on Mock Normal ∞ Pure")

    def get_current_features(self) -> list[float]:
        """Collect real 16-dim feature vector from Android metrics"""
        activity = PythonActivity.mActivity
        context = activity.getApplicationContext()

        # Battery
        intent = activity.registerReceiver(None, autoclass('android.content.IntentFilter')('android.intent.action.BATTERY_CHANGED'))
        battery_level = intent.getIntExtra(BatteryManager.EXTRA_LEVEL, -1)
        battery_scale = intent.getIntExtra(BatteryManager.EXTRA_SCALE, -1)
        battery_pct = battery_level / battery_scale if battery_scale > 0 else 0.5
        battery_temp = intent.getIntExtra(BatteryManager.EXTRA_TEMPERATURE, 0) / 10.0
        battery_voltage = intent.getIntExtra(BatteryManager.EXTRA_VOLTAGE, 0)

        # Network delta
        current_rx = TrafficStats.getTotalRxBytes()
        current_tx = TrafficStats.getTotalTxBytes()
        rx_delta = current_rx - self.last_rx
        tx_delta = current_tx - self.last_tx
        self.last_rx = current_rx
        self.last_tx = current_tx

        # Memory
        mem_info = ActivityManager.MemoryInfo()
        am = context.getSystemService(Context.ACTIVITY_SERVICE)
        am.getMemoryInfo(mem_info)
        mem_avail = mem_info.availMem / 1e6  # MB
        mem_total = mem_info.totalMem / 1e6
        mem_threshold = mem_info.threshold / 1e6

        # Running processes
        running_processes = len(am.getRunningAppProcesses())

        # WiFi connected
        wifi = context.getSystemService(Context.WIFI_SERVICE)
        wifi_connected = 1.0 if wifi.isWifiEnabled() else 0.0

        # Bluetooth
        bt = BluetoothAdapter.getDefaultAdapter()
        bt_enabled = 1.0 if bt and bt.isEnabled() else 0.0

        # Location
        loc = context.getSystemService(Context.LOCATION_SERVICE)
        loc_enabled = 1.0 if loc.isProviderEnabled(LocationManager.GPS_PROVIDER) or loc.isProviderEnabled(LocationManager.NETWORK_PROVIDER) else 0.0

        # Screen brightness (0-1)
        brightness = activity.getWindow().getAttributes().screenBrightness
        if brightness < 0:
            brightness = 0.5  # Default

        # Normalize/mock remaining for 16-dim
        features = [
            battery_pct,          # 0-1
            battery_temp / 50,    # ~0-1 normalized
            battery_voltage / 5000,  # ~0-1
            rx_delta / 1e6,       # MB delta normalized later
            tx_delta / 1e6,
            mem_avail / 10000,    # Rough total ~8-16GB
            mem_total / 16000,
            running_processes / 200,  # Typical 50-150
            wifi_connected,
            bt_enabled,
            loc_enabled,
            brightness,
            0.5,  # Placeholder sensor count
            0.5,  # Placeholder permission freq
            0.5,  # Placeholder file ops
            0.5   # Placeholder API calls
        ]

        # Simple normalization to ~0-1 (evolve with real min/max)
        return [max(0.0, min(1.0, f)) for f in features]

    def detect_anomalies(self) -> list[str]:
        features = self.get_current_features()
        input_tensor = torch.tensor([features], dtype=torch.float32)

        with torch.no_grad():
            output = self.model(input_tensor)
            error = nn.MSELoss()(output, input_tensor).item()

        if error > self.threshold:
            return [f"Real ML Anomaly Detected — Error {error:.4f} > {self.threshold} (Mobile Metrics Shadow)"]
        return []

# Global real detector
real_ml_detector = RealMLAnomalyDetector()

# In self_watchdog collect_anomalies:
# anomalies.extend(real_ml_detector.detect_anomalies())
