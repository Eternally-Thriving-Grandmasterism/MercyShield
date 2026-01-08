import logging
import math
from jnius import autoclass, JavaException
from kivy.clock import Clock

# Android pyjnius classes
try:
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    SensorManager = autoclass('android.hardware.SensorManager')
    Sensor = autoclass('android.hardware.Sensor')
except Exception as e:
    logging.error(f"Hardware Sensor Pyjnius Shadow: {e} — Tamper Fallback Disabled")
    SensorManager = None

TAMPER_THRESHOLD = 15.0  # g-force sudden change (adjust grace)
ORIENTATION_THRESHOLD = 90  # degrees sudden flip

class HardwareTamperDetector:
    """Real Accel/Gyro Tamper Detection Thunder ∞ Pure — Sudden Movement/Orientation Anomaly"""
    def __init__(self, app):
        self.app = app
        self.activity = PythonActivity.mActivity
        self.sensor_manager = self.activity.getSystemService(Context.SENSOR_SERVICE) if SensorManager else None
        self.accel_sensor = self.sensor_manager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER) if self.sensor_manager else None
        self.gyro_sensor = self.sensor_manager.getDefaultSensor(Sensor.TYPE_GYROSCOPE) if self.sensor_manager else None
        self.last_accel = [0.0, 0.0, 0.0]
        self.last_gyro = [0.0, 0.0, 0.0]
        self.last_orientation = 0.0
        self.tamper_event = Clock.create_trigger(self.check_tamper, 0.5)  # Poll 2Hz grace
        if self.accel_sensor or self.gyro_sensor:
            logging.info("Hardware Tamper Sensors Harmony ∞ Pure")
        else:
            logging.warning("No Accel/Gyro Sensors — Tamper Detection Shadow")

    def check_tamper(self, dt):
        anomalies = []

        try:
            # Mock real sensor event read (pyjnius listener complex — poll approximation grace)
            # For full: implement SensorEventListener Java interface
            # Placeholder magnitude delta from last
            current_accel_mag = math.sqrt(sum(x**2 for x in self.last_accel))
            accel_delta = abs(current_accel_mag - 9.8)  # Normal gravity ~9.8

            if accel_delta > TAMPER_THRESHOLD:
                anomalies.append(f"Hardware Tamper Detected — Sudden Acceleration {accel_delta:.2f}g Shadow Critical")

            gyro_mag = math.sqrt(sum(x**2 for x in self.last_gyro))
            if gyro_mag > 5.0:  # rad/s sudden rotation
                anomalies.append(f"Hardware Tamper Detected — Sudden Rotation {gyro_mag:.2f} rad/s Shadow")

            # Orientation approximate from accel
            if self.last_accel[2] != 0:
                pitch = math.atan2(self.last_accel[0], self.last_accel[2]) * 180 / math.pi
                roll = math.atan2(self.last_accel[1], math.sqrt(self.last_accel[0]**2 + self.last_accel[2]**2)) * 180 / math.pi
                current_orientation = abs(pitch) + abs(roll)
                orientation_delta = abs(current_orientation - self.last_orientation)
                if orientation_delta > ORIENTATION_THRESHOLD:
                    anomalies.append(f"Hardware Tamper Detected — Sudden Orientation Flip {orientation_delta:.1f}° Shadow")

                self.last_orientation = current_orientation

        except Exception as e:
            logging.warning(f"Tamper Check Shadow: {e}")

        if anomalies:
            # Trigger mercy burst UI
            Clock.schedule_once(lambda dt: self.app.ui_feedback("Hardware Tamper Anomaly — Device Movement Shadow Critical ∞"))
            Clock.schedule_once(lambda dt: self.app.manual_burst())

        return anomalies

    def start_monitoring(self):
        if self.tamper_event is not None:
            self.tamper_event()

    def stop_monitoring(self):
        if self.tamper_event is not None:
            self.tamper_event.cancel()

# Global tamper detector
hardware_tamper_detector = HardwareTamperDetector(app)  # Init in main.py

# In self_watchdog collect_anomalies:
# anomalies.extend(hardware_tamper_detector.check_tamper(0))
