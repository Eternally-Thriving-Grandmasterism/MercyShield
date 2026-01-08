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

# (GRU Hybrid model classes from previous—keep full)

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
        self.gru = nn.GRU(input_dim, hidden_dim, num_layers, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(hidden_dim * 2, input_dim)

    def forward(self, x):
        out, _ = self.gru(x)
        return self.fc(out[:, -1, :])

class SelfWatchdog:
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
        logging.info("Bidirectional GRU Hybrid Watchdog Activated ∞ Pure")
        self.ui_feedback("GRU Hybrid Model Initializing ∞ Pure")

    def ui_feedback(self, message, toast=False):
        def update(dt):
            if hasattr(self.app, 'status_label'):
                self.app.status_label.text += f'\n{message}'
        Clock.schedule_once(update)
        if toast:
            Toast.makeText(PythonActivity.mActivity, message, Toast.LENGTH_LONG).show()

    # collect_metrics, train_models, detect_anomalies from previous GRU hybrid

    def monitor_lattice(self):
        while self.running:
            try:
                vector = self.collect_metrics()
                self.history.append(vector)
                if len(self.history) > self.buffer_size:
                    self.history.pop(0)

                self.train_models()

                anomalies = self.detect_anomalies(vector)

                # Modular ESA Integration
                if self.council:
                    esa_anoms = self.council.esa_check_all_junctions()
                    if esa_anoms:
                        anomalies.extend(esa_anoms)
                        self.trigger_hotfix_recovery(esa_anoms)

                if anomalies:
                    logging.warning(f"Bi-GRU Hybrid + ESA Anomalies: {anomalies}")
                    self.ui_feedback(f"Hybrid Shield ∞: {len(anomalies)} Threats Flagged Pure", toast=True)
                    self.trigger_hotfix_recovery(anomalies)
                else:
                    logging.info("Hybrid + ESA Lattice Harmony Pure Divine")

                time.sleep(30)
            except Exception as e:
                logging.error(f"Hybrid Watchdog Shadow: {e} — Resurrect Eternal")
                time.sleep(10)

    def trigger_hotfix_recovery(self, anomalies):
        self.ui_feedback("Hybrid + ESA Hotfix Surge Divine Eternal")
        if hasattr(self.app, 'restart_vpn'):
            Clock.schedule_once(lambda dt: self.app.restart_vpn())
        if self.council:
            self.council.trigger_mercy_burst_recovery(anomalies)

    def stop(self):
        self.running = False
        self.thread.join(timeout=5)
        logging.info("Bi-GRU Hybrid Watchdog Deactivated Pure ∞")
