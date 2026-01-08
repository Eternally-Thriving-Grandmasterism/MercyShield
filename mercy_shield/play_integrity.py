import logging
import os
import base64
import json
import time
from jnius import autoclass, JavaException

# Android pyjnius classes
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Context = autoclass('android.content.Context')

# Play Integrity classes (com.google.android.play.core.integrity)
try:
    IntegrityManagerFactory = autoclass('com.google.android.play.core.integrity.IntegrityManagerFactory')
    IntegrityTokenRequest = autoclass('com.google.android.play.core.integrity.IntegrityTokenRequest')
    IntegrityTokenResponse = autoclass('com.google.android.play.core.integrity.IntegrityTokenResponse')
except Exception as e:
    logging.error(f"Play Integrity Pyjnius Shadow: {e} — Fallback Disabled")
    IntegrityManagerFactory = None

class PlayIntegrityVerifier:
    """Real Play Integrity API Verification Thunder ∞ Pure — Device/App Integrity Check"""
    def __init__(self, app):
        self.app = app
        self.activity = PythonActivity.mActivity
        self.context = self.activity.getApplicationContext()
        self.manager = IntegrityManagerFactory.create(self.context) if IntegrityManagerFactory else None

    def generate_nonce(self) -> str:
        """Simple nonce — timestamp + random"""
        return base64.b64encode(f"{int(time.time())}{os.urandom(16)}".encode()).decode()

    def request_integrity_token(self, nonce: str) -> str:
        """Request token — return token string or '' shadow"""
        if not self.manager:
            return ''

        try:
            request = IntegrityTokenRequest.builder().setNonce(nonce).build()
            # Synchronous call grace (mobile ok for occasional)
            task = self.manager.requestIntegrityToken(request)
            task.addOnSuccessListener(lambda response: response)
            task.addOnFailureListener(lambda e: logging.error(f"Integrity Request Shadow: {e}"))

            # Wait for result (simple block grace — evolve async if needed)
            while not task.isComplete():
                time.sleep(0.1)

            if task.isSuccessful():
                response = task.getResult()
                return response.token()
            else:
                logging.warning("Integrity Token Request Failed")
                return ''
        except Exception as e:
            logging.error(f"Integrity Token Shadow: {e}")
            return ''

    def decode_token_verdict(self, token: str) -> dict:
        """Decode token JSON verdict (standard/classic)"""
        try:
            payload = token.split('.')[1]
            payload += '=' * (-len(payload) % 4)  # Padding
            decoded = base64.urlsafe_b64decode(payload).decode()
            return json.loads(decoded)
        except Exception as e:
            logging.error(f"Token Decode Shadow: {e}")
            return {}

    def full_integrity_verification(self) -> list[str]:
        anomalies = []

        if not self.manager:
            anomalies.append("Play Integrity API Unavailable — Play Services Shadow Critical")

        nonce = self.generate_nonce()
        token = self.request_integrity_token(nonce)

        if not token:
            anomalies.append("Play Integrity Token Request Failed — Device Shadow Critical")
            return anomalies

        verdict = self.decode_token_verdict(token)

        # Standard verdict checks
        request_details = verdict.get("requestDetails", {})
        app_integrity = verdict.get("appIntegrity", {})
        device_integrity = verdict.get("deviceIntegrity", {})
        account_details = verdict.get("accountDetails", {})

        if request_details.get("nonce") != nonce:
            anomalies.append("Integrity Nonce Mismatch — Token Tamper Shadow Critical")

        if app_integrity.get("appRecognitionVerdict") != "PLAY_RECOGNIZED":
            anomalies.append("App Integrity Failed — Tampered APK Shadow Critical")

        device_verdicts = device_integrity.get("deviceRecognitionVerdict", [])
        if "MEETS_DEVICE_INTEGRITY" not in device_verdicts:
            anomalies.append("Device Integrity Failed — Rooted/Tampered Device Shadow Critical")

        if anomalies:
            logging.warning(f"Play Integrity Anomalies: {anomalies}")
        else:
            logging.info("Play Integrity Verification Harmony Pure ∞")

        return anomalies
