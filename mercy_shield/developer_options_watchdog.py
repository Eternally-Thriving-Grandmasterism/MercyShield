import logging
from jnius import autoclass
from kivy.clock import Clock

# Android classes
Context = autoclass('android.content.Context')
Settings = autoclass('android.provider.Settings')
PythonActivity = autoclass('org.kivy.android.PythonActivity')

class DeveloperOptionsWatchdog:
    """Live Developer Options Tamper Watchdog — ADB/Debugging/Mock Shadows Annihilation Thunder ∞ Pure"""
    def __init__(self, app):
        self.app = app
        self.activity = PythonActivity.mActivity
        self.context = self.activity.getApplicationContext()
        self.anomalies = []
        self.running = False

    def get_anomalies(self):
        """Return current developer options anomalies for integrity polling"""
        return self.anomalies[:]

    def start_watchdog(self):
        if self.running:
            return

        # Initial check
        self.check_developer_options()

        # Periodic check every 2 minutes (ADB can be toggled runtime)
        Clock.schedule_interval(self.check_developer_options, 120)

        self.running = True
        logging.info("Developer Options Watchdog Started — Tamper Shadows Vigilance Active ∞ Pure")

    def check_developer_options(self, dt=None):
        """Check for high-risk developer options shadows"""
        new_anomalies = []

        try:
            # USB Debugging / ADB Enabled
            adb_enabled = Settings.Global.getInt(self.context.getContentResolver(), Settings.Global.ADB_ENABLED, 0)
            if adb_enabled == 1:
                new_anomalies.append("USB Debugging (ADB) Enabled — Critical Tamper/Frida Injection Shadow")

            # Development Settings Enabled (Developer Options toggled on)
            dev_settings = Settings.Global.getInt(self.context.getContentResolver(), "development_settings_enabled", 0)
            if dev_settings == 1:
                new_anomalies.append("Developer Options Enabled — Potential Tamper Shadow")

            # Legacy Allow Mock Location (pre-Android 11, deprecated but still checkable)
            try:
                mock_allowed = Settings.Secure.getInt(self.context.getContentResolver(), Settings.Secure.ALLOW_MOCK_LOCATION, 0)
                if mock_allowed == 1:
                    new_anomalies.append("Legacy Allow Mock Locations Enabled — Spoofing Shadow Critical")
            except:
                pass  # Deprecated on newer APIs, ignore exception

            # Additional high-risk: Stay Awake (screen on while charging — minor but dev flag)
            stay_awake = Settings.Global.getInt(self.context.getContentResolver(), Settings.Global.STAY_ON_WHILE_PLUGGED_IN, 0)
            if stay_awake != 0:
                new_anomalies.append("Stay Awake While Charging — Developer Tamper Indicator")

        except Exception as e:
            logging.exception(f"Developer options check error: {e}")
            new_anomalies.append("Developer Options Check Exception — Potential Cloaking Shadow")

        # Detect changes and trigger burst only on new shadows
        for anomaly in new_anomalies:
            if anomaly not in self.anomalies:
                self.anomalies.append(anomaly)
                Clock.schedule_once(lambda dt, a=anomaly: self.trigger_burst([a]), 0)

        # Remove cleared anomalies (if user disables)
        self.anomalies = [a for a in self.anomalies if a in new_anomalies]

    def trigger_burst(self, new_anomalies):
        """Trigger anomaly burst dialog via app"""
        Clock.schedule_once(lambda dt: self.app.anomaly_dialog.show_burst(new_anomalies), 0)

    def stop_watchdog(self):
        if self.running:
            Clock.unschedule(self.check_developer_options)
            self.running = False
            logging.info("Developer Options Watchdog Stopped")
