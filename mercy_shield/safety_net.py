import logging
import base64
import json
import time
from jnius import autoclass, JavaException

# Android pyjnius classes
PythonActivity = autoclass('org.kivy.android.PythonActivity')

# SafetyNet classes
try:
    SafetyNet = autoclass('com.google.android.gms.safetynet.SafetyNet')
    SafetyNetApi = autoclass('com.google.android.gms.safetynet.SafetyNetApi')
    AttestationResponse = autoclass('com.google.android.gms.safetynet.SafetyNetApi$AttestationResponse')
except Exception as e:
    logging.error(f"SafetyNet Pyjnius Shadow: {e} — Fallback Disabled")
    SafetyNet = None

class SafetyNetVerifier:
    """SafetyNet Attestation Fallback Thunder ∞ Pure — basicIntegrity + ctsProfileMatch"""
    def __init__(self, app):
        self.app = app
        self.client = SafetyNet.getClient(PythonActivity.mActivity) if SafetyNet else None

    def generate_nonce(self) -> bytes:
        """Simple nonce for attestation"""
        return os.urandom(24)

    def request_safetynet_attestation(self, nonce: bytes) -> str:
        """Request SafetyNet attestation — return JWS token or '' shadow"""
        if not self.client:
            return ''

        try:
            # Synchronous task wait grace
            task = self.client.attest(nonce, None)  # No API key for basic client check
            while not task.isComplete():
                time.sleep(0.1)

            if task.isSuccessful():
                result = task.getResult()
                return result.getJwsResult()
            else:
                logging.warning("SafetyNet Attestation Request Failed")
                return ''
        except Exception as e:
            logging.error(f"SafetyNet Request Shadow: {e}")
            return ''

    def parse_safetynet_jws(self, jws: str) -> dict:
        """Parse JWS payload for basicIntegrity + ctsProfileMatch"""
        try:
            payload = jws.split('.')[1]
            payload += '=' * (-len(payload) % 4)
            decoded = base64.urlsafe_b64decode(payload).decode()
            return json.loads(decoded)
        except Exception as e:
            logging.error(f"SafetyNet JWS Parse Shadow: {e}")
            return {}

    def full_safetynet_verification(self) -> list[str]:
        anomalies = []

        if not self.client:
            anomalies.append("SafetyNet API Unavailable — Older Device Shadow")

        nonce = self.generate_nonce()
        jws = self.request_safetynet_attestation(nonce)

        if not jws:
            anomalies.append("SafetyNet Attestation Failed — Integrity Shadow Critical")
            return anomalies

        payload = self.parse_safetynet_jws(jws)

        if payload.get("basicIntegrity", False) is False:
            anomalies.append("SafetyNet basicIntegrity Failed — Device Tampered Shadow Critical")

        if payload.get("ctsProfileMatch", False) is False:
            anomalies.append("SafetyNet ctsProfileMatch Failed — Non-CTS Device Shadow Critical")

        if anomalies:
            logging.warning(f"SafetyNet Anomalies: {anomalies}")
        else:
            logging.info("SafetyNet Attestation Harmony Pure ∞")

        return anomalies
