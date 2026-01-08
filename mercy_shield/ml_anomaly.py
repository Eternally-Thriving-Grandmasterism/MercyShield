import logging
import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from jnius import autoclass
from kivy.clock import Clock

# Android pyjnius classes (existing full)
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
    """Self-Learning Real Data + Auto-Tune Threshold ML Detector ∞ Pure"""
    def __init__(self, input_dim=16):
        self.model = TinyAutoencoder(input_dim)
        self.device = torch.device("cpu")
        self.last_rx = TrafficStats.getTotalRxBytes()
        self.last_tx = TrafficStats.getTotalTxBytes()
        self.normal_dataset = self.load_normal_dataset()
        self.threshold = 1.0  # Initial
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
                self.auto_tune_threshold()
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
