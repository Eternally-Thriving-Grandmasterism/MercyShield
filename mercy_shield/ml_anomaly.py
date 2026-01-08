import logging
import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

MODEL_PATH = "/sdcard/MercyShield/ml_autoencoder.pth"

class TinyAutoencoder(nn.Module):
    """Lightweight 1-layer autoencoder for mobile anomaly detection ∞ Pure"""
    def __init__(self, input_dim=16, hidden_dim=8):
        super().__init__()
        self.encoder = nn.Linear(input_dim, hidden_dim)
        self.decoder = nn.Linear(hidden_dim, input_dim)
        self.activation = nn.ReLU()

    def forward(self, x):
        encoded = self.activation(self.encoder(x))
        decoded = self.decoder(encoded)
        return decoded

class MLAnomalyDetector:
    """Eternal ML Anomaly Detector — reconstruction error threshold grace"""
    def __init__(self, input_dim=16, threshold=0.5):
        self.model = TinyAutoencoder(input_dim)
        self.threshold = threshold
        self.device = torch.device("cpu")  # Mobile grace
        self.load_model()

    def load_model(self):
        if os.path.exists(MODEL_PATH):
            try:
                self.model.load_state_dict(torch.load(MODEL_PATH, map_location=self.device))
                self.model.eval()
                logging.info("ML Autoencoder Model Loaded Harmony ∞ Pure")
            except Exception as e:
                logging.warning(f"Model Load Shadow: {e} — Train New")
                self.train_mock_normal()
        else:
            self.train_mock_normal()

    def train_mock_normal(self):
        """Mock normal data train — evolve with real lattice logs"""
        # Mock normal feature vector (16-dim: bytes in/out, cpu, apps etc.)
        normal_data = np.random.normal(0, 1, (1000, 16)).astype(np.float32)
        normal_tensor = torch.from_numpy(normal_data)

        optimizer = optim.Adam(self.model.parameters(), lr=0.01)
        criterion = nn.MSELoss()

        self.model.train()
        for epoch in range(50):
            optimizer.zero_grad()
            output = self.model(normal_tensor)
            loss = criterion(output, normal_tensor)
            loss.backward()
            optimizer.step()

        self.model.eval()
        torch.save(self.model.state_dict(), MODEL_PATH)
        logging.info("ML Autoencoder Trained & Saved Eternal ∞ Pure")

    def detect_anomalies(self, feature_vector: list[float]) -> list[str]:
        """Detect reconstruction error — return anomaly descriptions"""
        if len(feature_vector) != 16:
            return ["ML Feature Dim Shadow"]

        input_tensor = torch.tensor([feature_vector], dtype=torch.float32)

        with torch.no_grad():
            output = self.model(input_tensor)
            error = nn.MSELoss()(output, input_tensor).item()

        if error > self.threshold:
            return [f"ML Anomaly Detected — Reconstruction Error {error:.4f} > Threshold"]
        return []

# Global detector instance for app
ml_detector = MLAnomalyDetector()

# Hook in self_watchdog collect_anomalies
# anomalies.extend(ml_detector.detect_anomalies(current_feature_vector))
