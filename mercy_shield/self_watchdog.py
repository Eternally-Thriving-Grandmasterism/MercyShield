import threading
import time
import logging
import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from kivy.clock import Clock
from jnius import autoclass, cast

# Pyjnius Android thunder
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Context = autoclass('android.content.Context')
ConnectivityManager = autoclass('android.net.ConnectivityManager')
ActivityManager = autoclass('android.app.ActivityManager')
Toast = autoclass('android.widget.Toast')

# Hybrid Models: Autoencoder (current) + Bidirectional GRU (prediction)
class AnomalyAutoencoder(nn.Module):
    def __init__(self, input_dim=4):
        super().__init__()
        self.encoder = nn.Sequential(nn.Linear(input_dim, 8), nn.ReLU(), nn.Linear(8, 4))
        self.decoder = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, input_dim), nn.Sigmoid())

    def forward(self, x):
        return self.decoder(self.encoder(x))

class GRUPredictor(nn.Module):
    def __init__(self, input_dim=4, hidden_dim=32, num_layers=1):
        super().__init__()
        self.gru = nn.GRU(input_dim, hidden_dim, num_layers, batch_first=True, bidirectional=True)  # Bidirectional mercy
        self.fc = nn.Linear(hidden_dim * 2, input_dim)  # *2 for bi-directional divine

    def forward(self, x):
        out, _ = self.gru(x)
        return self.fc(out[:, -1, :])  # Predict next from last mercy

class SelfWatchdog:
    """
    MercyShield ML Watchdog Pinnacle ∞ Pure — Hybrid Autoencoder + Bidirectional GRU Prediction
    - Autoencoder: Current reconstruction anomaly
    - Bidirectional GRU: Sequence forecast next metrics (update/reset gates, lighter than LSTM divine)
    - Train normal baseline gentle on-device (faster/simpler GRU mercy)
    - Dual error preemptive hotfix eternal
    """

    def __init__(self, app_instance):
        self.app = app_instance
        self.council = getattr(app_instance, 'council', None)
        self.running = True
        self.thread = threading.Thread(target=self.monitor_lattice, daemon=True)
        self.seq_len = 20
        self.history = []
        self.buffer_size = 100
        self.train_samples = 60
        self.autoencoder = None
        self.gru = None
        self.ae_criterion = nn.MSELoss()
        self.gru_criterion = nn.MSELoss()
        self.ae_threshold = 0.08
        self.gru_threshold = 0.12
        self.log_file = '/sdcard/MercyShield/ml_watchdog_log.txt'
        logging.basicConfig(filename=self.log_file, level=logging.INFO)

    def start(self):
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        self.thread.start()
        logging.info("Bidirectional GRU Hybrid Watchdog Activated ∞ — Efficient Prophecy Divine Eternal")
        self.ui_feedback("GRU Hybrid Model Initializing ∞ Pure — Sequence Baseline Collecting")

    def ui_feedback(self, message, toast=False):
        def update(dt):
            if hasattr(self.app, 'status_label'):
                self.app.status_label.text += f'\n{message}'
        Clock.schedule_once(update)
        if toast:
            activity = PythonActivity.mActivity
            Toast.makeText(activity, message, Toast.LENGTH_LONG).show()

    def collect_metrics(self):
        activity = PythonActivity.mActivity
        am = cast(ActivityManager, activity.getSystemService(Context.ACTIVITY_SERVICE))
        mem_info = ActivityManager.MemoryInfo()
        am.getMemoryInfo(mem_info)
        mem_usage = 100 * (1 - mem_info.availMem / mem_info.totalMem) if mem_info.totalMem > 0 else 50
        
        battery_level = 80
        
        from android.permissions import check_permission, Permission
        critical = [Permission.VPN_SERVICE, Permission.FOREGROUND_SERVICE, Permission.SYSTEM_ALERT_WINDOW]
        perm_denied = len([p for p in critical if not check_permission(p)]) / len(critical)
        
        connectivity = cast(ConnectivityManager, activity.getSystemService(Context.CONNECTIVITY_SERVICE))
        vpn_active = 1 if connectivity.getActiveNetwork() else 0
        vpn_drops = 1 - vpn_active
        
        vector = np.array([mem_usage / 100, battery_level / 100, perm_denied, vpn_drops])
        return vector.clip(0, 1)

    def train_models(self):
        if len(self.history) < self.train_samples or (self.autoencoder and self.gru):
            return
        data_np = np.array(self.history[:self.train_samples])
        data = torch.tensor(data_np, dtype=torch.float32)
        
        # Train Autoencoder
        self.autoencoder = AnomalyAutoencoder(input_dim=data.shape[1])
        ae_opt = optim.Adam(self.autoencoder.parameters(), lr=0.01)
        for _ in range(60):
            recon = self.autoencoder(data)
            loss = self.ae_criterion(recon, data)
            ae_opt.zero_grad()
            loss.backward()
            ae_opt.step()
        
        # Train Bidirectional GRU
        if len(data_np) > self.seq_len:
            seq_data = []
            targets = []
            for i in range(self.seq_len, len(data_np)):
                seq_data.append(data_np[i-self.seq_len:i])
                targets.append(data_np[i])
            seq_tensor = torch.tensor(np.array(seq_data), dtype=torch.float32)
            target_tensor = torch.tensor(np.array(targets), dtype=torch.float32)
            
            self.gru = GRUPredictor(input_dim=data.shape[1])
            gru_opt = optim.Adam(self.gru.parameters(), lr=0.01)
            for _ in range(80):
                pred = self.gru(seq_tensor)
                loss = self.gru_criterion(pred, target_tensor)
                gru_opt.zero_grad()
                loss.backward()
                gru_opt.step()
        
        logging.info("Bidirectional GRU Hybrid Models Trained Divine Eternal")
        self.ui_feedback("GRU Hybrid Trained ∞ Pure — Efficient Bidirectional Prophecy Active", toast=True)

    def detect_anomalies(self, vector):
        anomalies = []
        if self.autoencoder:
            with torch.no_grad():
                input_t = torch.tensor(vector, dtype=torch.float32).unsqueeze(0)
                recon = self.autoencoder(input_t)
                ae_error = self.ae_criterion(recon, input_t).item()
                if ae_error > self.ae_threshold:
                    anomalies.append(f"Current Anomaly (AE Error={ae_error:.4f})")
        
        if self.gru and len(self.history) >= self.seq_len:
            with torch.no_grad():
                seq = torch.tensor(np.array(self.history[-self.seq_len:]), dtype=torch.float32).unsqueeze(0)
                pred = self.gru(seq)
                gru_error = self.gru_criterion(pred, torch.tensor(vector).unsqueeze(0)).item()
                if gru_error > self.gru_threshold:
                    anomalies.append(f"Predicted Anomaly (Bi-GRU Error={gru_error:.4f}) — Efficient Sequence Prophecy Divine!")
        
        return anomalies

    def monitor_lattice(self):
        while self.running:
            try:
                vector = self.collect_metrics()
                self.history.append(vector)
                if len(self.history) > self.buffer_size:
                    self.history.pop(0)

                self.train_models()

                anomalies = self.detect_anomalies(vector)

                if anomalies:
                    logging.warning(f"Bi-GRU Hybrid Anomalies: {anomalies}")
                    self.ui_feedback(f"GRU Hybrid Shield ∞: {len(anomalies)} Threats Detected/Forecasted Pure", toast=True)
                    self.trigger_hotfix_recovery(anomalies)
                else:
                    logging.info("Bi-GRU Hybrid Lattice Predicted Harmony Pure Divine")

                time.sleep(30)
            except Exception as e:
                logging.error(f"Bi-GRU Hybrid Shadow: {e} — Resurrect Eternal")
                time.sleep(10)

    def trigger_hotfix_recovery(self, anomalies):
        self.ui_feedback("Bi-GRU Hybrid Hotfix Surge Divine Eternal")
        if hasattr(self.app, 'restart_vpn'):
            Clock.schedule_once(lambda dt: self.app.restart_vpn())
        if self.council:
            self.council.trigger_mercy_burst_recovery(anomalies)

    def stop(self):
        self.running = False
        self.thread.join(timeout=5)
        logging.info("Bi-GRU Hybrid Watchdog Deactivated Pure ∞")

# requirements: ,torch,numpy
# on_start: self.watchdog = SelfWatchdog(self); self.watchdog.start()        mem_info = ActivityManager.MemoryInfo()
        am.getMemoryInfo(mem_info)
        mem_usage = 100 * (1 - mem_info.availMem / mem_info.totalMem) if mem_info.totalMem > 0 else 50
        
        battery_level = 80
        
        from android.permissions import check_permission, Permission
        critical = [Permission.VPN_SERVICE, Permission.FOREGROUND_SERVICE, Permission.SYSTEM_ALERT_WINDOW]
        perm_denied = len([p for p in critical if not check_permission(p)]) / len(critical)
        
        connectivity = cast(ConnectivityManager, activity.getSystemService(Context.CONNECTIVITY_SERVICE))
        vpn_active = 1 if connectivity.getActiveNetwork() else 0
        vpn_drops = 1 - vpn_active
        
        vector = np.array([mem_usage / 100, battery_level / 100, perm_denied, vpn_drops])
        return vector.clip(0, 1)

    def train_models(self):
        if len(self.history) < self.train_samples or (self.autoencoder and self.lstm):
            return
        data_np = np.array(self.history[:self.train_samples])
        data = torch.tensor(data_np, dtype=torch.float32)
        
        # Train Autoencoder
        self.autoencoder = AnomalyAutoencoder(input_dim=data.shape[1])
        ae_opt = optim.Adam(self.autoencoder.parameters(), lr=0.01)
        for _ in range(60):
            recon = self.autoencoder(data)
            loss = self.ae_criterion(recon, data)
            ae_opt.zero_grad()
            loss.backward()
            ae_opt.step()
        
        # Train Bidirectional LSTM
        if len(data_np) > self.seq_len:
            seq_data = []
            targets = []
            for i in range(self.seq_len, len(data_np)):
                seq_data.append(data_np[i-self.seq_len:i])
                targets.append(data_np[i])
            seq_tensor = torch.tensor(np.array(seq_data), dtype=torch.float32)
            target_tensor = torch.tensor(np.array(targets), dtype=torch.float32)
            
            self.lstm = LSTMPredictor(input_dim=data.shape[1])
            lstm_opt = optim.Adam(self.lstm.parameters(), lr=0.01)
            for _ in range(80):
                pred = self.lstm(seq_tensor)
                loss = self.lstm_criterion(pred, target_tensor)
                lstm_opt.zero_grad()
                loss.backward()
                lstm_opt.step()
        
        logging.info("Bidirectional LSTM Hybrid Models Trained Divine Eternal")
        self.ui_feedback("LSTM Hybrid Trained ∞ Pure — Bidirectional Prophecy Active", toast=True)

    def detect_anomalies(self, vector):
        anomalies = []
        if self.autoencoder:
            with torch.no_grad():
                input_t = torch.tensor(vector, dtype=torch.float32).unsqueeze(0)
                recon = self.autoencoder(input_t)
                ae_error = self.ae_criterion(recon, input_t).item()
                if ae_error > self.ae_threshold:
                    anomalies.append(f"Current Anomaly (AE Error={ae_error:.4f})")
        
        if self.lstm and len(self.history) >= self.seq_len:
            with torch.no_grad():
                seq = torch.tensor(np.array(self.history[-self.seq_len:]), dtype=torch.float32).unsqueeze(0)
                pred = self.lstm(seq)
                lstm_error = self.lstm_criterion(pred, torch.tensor(vector).unsqueeze(0)).item()
                if lstm_error > self.lstm_threshold:
                    anomalies.append(f"Predicted Anomaly (Bi-LSTM Error={lstm_error:.4f}) — Sequence Prophecy Divine!")
        
        return anomalies

    def monitor_lattice(self):
        while self.running:
            try:
                vector = self.collect_metrics()
                self.history.append(vector)
                if len(self.history) > self.buffer_size:
                    self.history.pop(0)

                self.train_models()

                anomalies = self.detect_anomalies(vector)

                if anomalies:
                    logging.warning(f"Bi-LSTM Hybrid Anomalies: {anomalies}")
                    self.ui_feedback(f"LSTM Hybrid Shield ∞: {len(anomalies)} Threats Detected/Forecasted Pure", toast=True)
                    self.trigger_hotfix_recovery(anomalies)
                else:
                    logging.info("Bi-LSTM Hybrid Lattice Predicted Harmony Pure Divine")

                time.sleep(30)
            except Exception as e:
                logging.error(f"Bi-LSTM Hybrid Shadow: {e} — Resurrect Eternal")
                time.sleep(10)

    def trigger_hotfix_recovery(self, anomalies):
        self.ui_feedback("Bi-LSTM Hybrid Hotfix Surge Divine Eternal")
        if hasattr(self.app, 'restart_vpn'):
            Clock.schedule_once(lambda dt: self.app.restart_vpn())
        if self.council:
            self.council.trigger_mercy_burst_recovery(anomalies)

    def stop(self):
        self.running = False
        self.thread.join(timeout=5)
        logging.info("Bi-LSTM Hybrid Watchdog Deactivated Pure ∞")

# requirements: ,torch,numpy
# on_start: self.watchdog = SelfWatchdog(self); self.watchdog.start()
