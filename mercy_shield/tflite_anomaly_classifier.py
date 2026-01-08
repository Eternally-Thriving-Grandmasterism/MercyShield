import logging
import numpy as np
try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    import tensorflow.lite as tflite  # Fallback for desktop testing
from kivy.app import App

class TFLiteAnomalyClassifier:
    """Advanced TensorFlow Lite On-Device ML Anomaly Classifier — Neural Risk Scoring Thunder ∞ Pure"""
    def __init__(self, app):
        self.app = app
        model_path = "anomaly_classifier.tflite"  # Bundled in app root — train & place before build
        try:
            self.interpreter = tflite.Interpreter(model_path=model_path, num_threads=4)
            self.interpreter.allocate_tensors()
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            logging.info("TFLite Anomaly Classifier Loaded — Divine Neural Thunder Active ∞ Pure")
        except Exception as e:
            logging.exception(f"TFLite model load failed: {e} — Falling back to legacy scoring")
            self.interpreter = None

        # Expected feature vector size (adjust to your trained model input)
        self.feature_size = 50
        self.threshold_critical = 0.8  # ML risk >= this = compromised (0.0-1.0 sigmoid output)

        # Mapping of known anomaly keys to feature indices (partial — expand as needed)
        self.anomaly_to_index = {
            "No Light Sensor": 0,
            "No Accelerometer": 1,
            "Low Count Emulator Shadow": 2,
            "No GPS Hardware Feature": 3,
            "No Cellular Telephony": 4,
            "Frida Server Detected": 5,
            "Emulator Build Props Detected": 6,
            "Generic Fingerprint": 7,
            "ro.kernel.qemu=1": 8,
            "Test-Keys Build": 9,
            "Root Binary": 10,
            "Root Management App": 11,
            "Magisk Mounts Detected": 12,
            "USB Debugging (ADB) Enabled": 13,
            "Live Mock Location Detected": 14,
            # Add more up to 49...
        }

    def extract_features(self, anomalies: list[str]) -> np.ndarray:
        """Convert anomaly list to fixed-size feature vector (binary presence)"""
        features = np.zeros(self.feature_size, dtype=np.float32)
        for anomaly in anomalies:
            for key, idx in self.anomaly_to_index.items():
                if key in anomaly:
                    features[idx] = 1.0
                    break
        # Add numeric features if needed (e.g., sensor count / max)
        return features[np.newaxis, :]  # Add batch dimension

    def predict_risk(self, anomalies: list[str]) -> float:
        """Run TFLite inference — return risk score 0.0 (genuine) to 1.0 (compromised)"""
        if not self.interpreter or not anomalies:
            return 0.0

        input_data = self.extract_features(anomalies)
        try:
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            self.interpreter.invoke()
            risk = self.interpreter.get_tensor(self.output_details[0]['index'])[0][0]
            return float(risk)
        except Exception as e:
            logging.exception(f"TFLite inference error: {e}")
            return 0.0

    # Future: on-device fine-tuning hook (advanced domino)
    # def fine_tune(self, features, label): ...

# Example model training script (run on desktop — generate anomaly_classifier.tflite)
"""
import tensorflow as tf
import numpy as np

# Dummy training data — replace with real labeled device datasets
X_train = np.random.rand(1000, 50).astype(np.float32)  # 1000 samples, 50 features
y_train = np.random.randint(0, 2, 1000).astype(np.float32)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(50,)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=20, validation_split=0.2)

# Convert to TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open('anomaly_classifier.tflite', 'wb') as f:
    f.write(tflite_model)

# Place generated file in project root before build
"""
