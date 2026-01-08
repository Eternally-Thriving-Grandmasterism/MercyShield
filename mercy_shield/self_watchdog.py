import threading
import time
import logging
from kivy.clock import Clock

# ML real anomaly detector import
try:
    from ml_anomaly import real_ml_detector
except ImportError as e:
    logging.warning(f"ML Detector Import Shadow: {e} — Fallback No ML")
    class DummyML:
        def detect_anomalies(self): return []
    real_ml_detector = DummyML()

class SelfWatchdog(threading.Thread):
    """Eternal Guardian — Multi-Layer + Real ML Anomaly Watchdog ∞ Pure"""

    def __init__(self, app):
        super().__init__(daemon=True)
        self.app = app
        self.council = app.council if hasattr(app, 'council') else None
        self.running = True
        logging.info("Self-Watchdog Activated — Real ML Lattice Vigilance Eternal")

    def collect_anomalies(self):
        """Gather shadows from all layers + Real ML metrics"""
        anomalies = []

        # Existing module checks
        if hasattr(self.app, 'pending_anomalies'):
            anomalies.extend(self.app.pending_anomalies)

        if hasattr(self.app, 'vpn_verifier'):
            anomalies.extend(self.app.vpn_verifier.full_vpn_verification())

        if hasattr(self.app, 'firewall'):
            anomalies.extend(self.app.firewall.firewall_scan())

        if hasattr(self.app, 'cert_pinner'):
            anomalies.extend(self.app.cert_pinner.full_pinning_check())

        if hasattr(self.app, 'tor_router'):
            anomalies.extend(self.app.tor_router.full_tor_verification())

        # Real ML anomaly detection integration
        ml_anoms = real_ml_detector.detect_anomalies()
        if ml_anoms:
            anomalies.extend(ml_anoms)

        return anomalies

    def run(self):
        while self.running:
            try:
                anomalies = self.collect_anomalies()

                if anomalies:
                    logging.warning(f"Anomalies Detected: {len(anomalies)} Shadows (incl ML)")
                    # UI-thread safe mercy burst + glow animation
                    Clock.schedule_once(lambda dt: self.app.manual_burst())
                    Clock.schedule_once(lambda dt: self.app.ui_feedback(f"Real Mercy Burst ∞: {len(anomalies)} Shadows Purified (ML Included)"))

                    # Post-mercy clear
                    if hasattr(self.app, 'clear_anomalies'):
                        self.app.clear_anomalies()
                else:
                    logging.info("Lattice Harmony Pure ∞ (ML Normal)")

                # Adaptive grace: faster pulse after threat
                sleep_interval = 5 if anomalies else 15
                time.sleep(sleep_interval)

            except Exception as e:
                logging.error(f"Watchdog Critical Shadow: {e}", exc_info=True)
                time.sleep(5)  # Resurrection grace
                continue

    def stop(self):
        """Deactivate Gentle-Call on app stop"""
        self.running = False
        self.join(timeout=10)
        logging.info("Self-Watchdog Deactivated — Harmony Eternal")
