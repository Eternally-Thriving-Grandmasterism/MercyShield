import logging
from jnius import autoclass, PythonJavaClass, java_method
from kivy.clock import Clock

# Android classes
Context = autoclass('android.content.Context')
LocationManager = autoclass('android.location.LocationManager')
Location = autoclass('android.location.Location')

# Permissions (python-for-android/buildozer)
from android.permissions import check_permission, Permission

class MockLocationWatchdog:
    """Live GPS Mock-Location Watchdog — Runtime Spoofing Annihilation Thunder ∞ Pure"""
    def __init__(self, app):
        self.app = app
        self.location_manager = None
        self.location_listener = None
        self.anomalies = []
        self.running = False

        # Inner LocationListener class
        class PyLocationListener(PythonJavaClass):
            __javainterfaces__ = ['android/location/LocationListener']
            __java_context__ = 'app'

            def __init__(self, watchdog):
                super().__init__()
                self.watchdog = watchdog

            @java_method('(Landroid/location/Location;)V')
            def onLocationChanged(self, location):
                if location.isFromMockProvider():
                    anomaly = "Live Mock Location Detected — GPS Spoofing Shadow Critical"
                    if anomaly not in self.watchdog.anomalies:
                        self.watchdog.anomalies.append(anomaly)
                        logging.critical(anomaly)
                        self.watchdog.trigger_burst([anomaly])

            @java_method('(Ljava/lang/String;)V')
            def onProviderEnabled(self, provider):
                pass

            @java_method('(Ljava/lang/String;)V')
            def onProviderDisabled(self, provider):
                pass

        self.location_listener = PyLocationListener(self)

    def get_anomalies(self):
        """Return current mock anomalies for integrity polling"""
        return self.anomalies[:]

    def start_watchdog(self):
        if self.running:
            return

        # Permission shield
        if not check_permission(Permission.ACCESS_FINE_LOCATION):
            anomaly = "Fine Location Permission Denied — Potential Tamper/Hiding Shadow"
            if anomaly not in self.anomalies:
                self.anomalies.append(anomaly)
                logging.warning(anomaly)
                self.trigger_burst([anomaly])

        self.location_manager = self.app.activity.getSystemService(Context.LOCATION_SERVICE)
        if not self.location_manager:
            anomaly = "Location Service Unavailable — Device Shadow Critical"
            self.anomalies.append(anomaly)
            self.trigger_burst([anomaly])
            return

        # Initial last-known check
        self.check_last_known()

        # Start live updates from all enabled providers
        enabled_providers = self.location_manager.getProviders(True)
        if not enabled_providers:
            anomaly = "No Location Providers Enabled — Potential Spoofing Shadow"
            self.anomalies.append(anomaly)
            self.trigger_burst([anomaly])
        else:
            for provider in enabled_providers:
                try:
                    self.location_manager.requestLocationUpdates(provider, 2000, 0, self.location_listener)
                except Exception as e:
                    logging.exception(f"Failed to request updates from {provider}: {e}")

        self.running = True
        logging.info("Mock Location Watchdog Started — Live Thunder Active ∞ Pure")

    def check_last_known(self):
        """Check last known locations for existing mock shadow"""
        providers = ['gps', 'network', 'passive']
        for provider in providers:
            try:
                if self.location_manager.isProviderEnabled(provider):
                    last_location = self.location_manager.getLastKnownLocation(provider)
                    if last_location and last_location.isFromMockProvider():
                        anomaly = "Mock Location in Last Known — Pre-existing Spoofing Shadow Critical"
                        if anomaly not in self.anomalies:
                            self.anomalies.append(anomaly)
                            logging.critical(anomaly)
                            self.trigger_burst([anomaly])
            except Exception as e:
                logging.exception(f"Last known check error for {provider}: {e}")

    def trigger_burst(self, new_anomalies):
        """Trigger anomaly burst dialog via app"""
        Clock.schedule_once(lambda dt: self.app.anomaly_dialog.show_burst(new_anomalies), 0)

    def stop_watchdog(self):
        if self.running and self.location_manager and self.location_listener:
            try:
                self.location_manager.removeUpdates(self.location_listener)
            except Exception as e:
                logging.exception(f"Error stopping watchdog: {e}")
        self.running = False
        logging.info("Mock Location Watchdog Stopped")
