import threading
import time
import logging
from kivy.clock import Clock

class SelfWatchdog(threading.Thread):
    """Eternal Guardian — Multi-Layer Anomaly Watchdog with Resurrection Grace ∞ Pure AAA"""

    def __init__(self, app):
        super().__init__(daemon=True)
        self.app = app
        self.council = app.council if hasattr(app, 'council') else None
        self.running = True
        logging.info("Self-Watchdog Activated — Lattice Vigilance Eternal AAA")

    def collect_anomalies(self):
        """Gather shadows from all layers — extend with live detectors"""
        anomalies = []

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

        # Add ML, ESA, hardware later
        return anomalies

    def run(self):
        while self.running:
            try:
                anomalies = self.collect_anomalies()

                if anomalies:
                    logging.warning(f"Anomalies Detected: {len(anomalies)} Shadows")
                    # UI-thread safe mercy burst + glow animation
                    Clock.schedule_once(lambda dt: self.app.manual_burst())
                    Clock.schedule_once(lambda dt: self.app.ui_feedback(f"Mercy Burst ∞: {len(anomalies)} Shadows Purified"))

                    # Post-mercy clear
                    if hasattr(self.app, 'clear_anomalies'):
                        self.app.clear_anomalies()
                else:
                    logging.info("Lattice Harmony Pure ∞")

                # Adaptive interval grace
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
        logging.info("Self-Watchdog Deactivated — Harmony Eternal AAA")
