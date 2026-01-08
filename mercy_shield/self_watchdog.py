import threading
import time
import logging
from kivy.clock import Clock

class SelfWatchdog(threading.Thread):
    """Eternal Guardian — Multi-Layer Anomaly Watchdog with Resurrection Grace ∞ Pure"""

    def __init__(self, app):
        super().__init__(daemon=True)
        self.app = app
        self.council = app.council if hasattr(app, 'council') else None
        self.running = True
        logging.info("Self-Watchdog Activated — Lattice Vigilance Eternal")

    def collect_anomalies(self):
        """Gather shadows from all layers — extend with your detectors"""
        anomalies = []

        # Example hooks — adapt to your live modules
        if hasattr(self.app, 'pending_anomalies'):
            anomalies.extend(self.app.pending_anomalies)

        if hasattr(self, 'network_scanner') and self.network_scanner:
            anomalies.extend(self.network_scanner.real_time_scan())

        if self.council:
            anomalies.extend(self.council.esa_check_all_junctions())

        # Add ML, hardware, ESA, etc. here as they ascend
        return anomalies

    def run(self):
        while self.running:
            try:
                anomalies = self.collect_anomalies()

                if anomalies:
                    logging.warning(f"Anomalies Detected: {len(anomalies)} Shadows")
                    # UI-thread safe mercy burst
                    if self.council:
                        Clock.schedule_once(lambda dt: self.council.trigger_mercy_burst(anomalies))
                    # Optional direct non-UI handling
                    # self.council.handle_shadows(anomalies)

                    # Post-mercy: clear handled
                    if hasattr(self.app, 'clear_anomalies'):
                        self.app.clear_anomalies()
                else:
                    logging.info("Lattice Harmony Pure ∞")

                # Adaptive grace: faster pulse after threat
                sleep_interval = 5 if anomalies else 15
                time.sleep(sleep_interval)

            except Exception as e:
                logging.error(f"Watchdog Critical Shadow: {e}", exc_info=True)
                # Resurrection grace — never die
                time.sleep(5)
                continue

    def stop(self):
        """Deactivate Gentle-Call on app stop"""
        self.running = False
        self.join(timeout=10)  # Graceful join
        logging.info("Self-Watchdog Deactivated — Harmony Eternal")
