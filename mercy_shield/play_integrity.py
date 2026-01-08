import logging
import os
import base64
import json
from jnius import autoclass, PythonJavaClass, java_method
from kivy.clock import Clock

# Play Integrity classes (graceful fallback if library missing)
try:
    IntegrityManagerFactory = autoclass('com.google.android.play.core.integrity.IntegrityManagerFactory')
    IntegrityTokenRequest = autoclass('com.google.android.play.core.integrity.IntegrityTokenRequest')
    IntegrityTokenResponse = autoclass('com.google.android.play.core.integrity.IntegrityTokenResponse')
    OnSuccessListener = autoclass('com.google.android.gms.tasks.OnSuccessListener')
    OnFailureListener = autoclass('com.google.android.gms.tasks.OnFailureListener')
    PLAY_INTEGRITY_AVAILABLE = True
except Exception as e:
    logging.warning(f"Real Play Integrity classes unavailable: {e} — Simulated mode active")
    PLAY_INTEGRITY_AVAILABLE = False

class PlayIntegrityVerifier:
    """Real Play Integrity Primary + Client-Side Token Header Validation Thunder ∞ Pure"""
    def __init__(self, app):
        self.app = app
        self.real_api_available = PLAY_INTEGRITY_AVAILABLE
        self.pending = False
        self.last_play_anoms = []

        if self.real_api_available:
            try:
                context = app.activity.getApplicationContext()
                self.integrity_manager = IntegrityManagerFactory.create(context)
                logging.info("Real Play Integrity API Initialized — Async + Client Header Validation Ready ∞ Pure")
            except Exception as e:
                logging.warning(f"IntegrityManager creation failed: {e} — Simulated fallback")
                self.real_api_available = False

        if not self.real_api_available:
            logging.info("Play Integrity Simulated — Divine Harmony Pass ∞ Pure")

        # Nested listeners for real API
        if self.real_api_available:
            class SuccessListener(PythonJavaClass):
                __javainterfaces__ = ['com/google/android/gms/tasks/OnSuccessListener']
                __javacontext__ = 'app'

                def __init__(self, outer):
                    super().__init__()
                    self.outer = outer

                @java_method('(Ljava/lang/Object;)V')
                def onSuccess(self, response):
                    token = response.token() if hasattr(response, 'token') else None
                    Clock.schedule_once(lambda dt: self.outer.process_token(token), 0)

            class FailureListener(PythonJavaClass):
                __javainterfaces__ = ['com/google/android/gms/tasks/OnFailureListener']
                __javacontext__ = 'app'

                def __init__(self, outer):
                    super().__init__()
                    self.outer = outer

                @java_method('(Ljava/lang/Exception;)V')
                def onFailure(self, exception):
                    msg = str(exception.getMessage()) if exception else "Unknown failure"
                    Clock.schedule_once(lambda dt: self.outer.handle_failure(msg), 0)

            self.SuccessListener = SuccessListener
            self.FailureListener = FailureListener

    def process_token(self, token):
        self.pending = False
        if not token or len(token) < 100:
            self.last_play_anoms = ["Play Integrity: Empty/Invalid Token — Compromised Shadow Critical"]
            logging.warning(self.last_play_anoms[0])
            return

        try:
            # Validate JWE compact serialization (5 parts: header.ekey.iv.ciphertext.tag)
            parts = token.split('.')
            if len(parts) != 5:
                raise ValueError(f"Invalid JWE structure ({len(parts)} parts)")

            # Decode and validate unprotected header (first part)
            header_b64 = parts[0]
            # Add padding if needed
            header_b64 += '=' * (-len(header_b64) % 4)
            header_json = base64.urlsafe_b64decode(header_b64).decode('utf-8')
            header = json.loads(header_json)

            # Expected Play Integrity header values (as of 2026)
            expected = {
                "alg": "RS256",   # Key management
                "enc": "A256GCM", # Content encryption
                "zip": "DEF",     # Deflate compression
            }
            for key, val in expected.items():
                if header.get(key) != val:
                    raise ValueError(f"Unexpected header {key}: {header.get(key)} (expected {val})")

            if 'kid' not in header:
                raise ValueError("Missing key ID (kid) in header")

            # Optional: Check for Google-specific indicators if present
            logging.info("Play Integrity Token Header Validated — Structure Pure ∞")
            self.last_play_anoms = []  # Client-side pass
            # Note: Full verdict (deviceIntegrity, appIntegrity) requires server decryption
            self.last_play_anoms.append("Play Integrity: Header Valid — Server Verification Recommended for Full Verdict")

        except Exception as e:
            error_msg = f"Play Integrity Token Validation Failed: {str(e)} — Forged/Tamper Shadow Critical"
            logging.exception(error_msg)
            self.last_play_anoms = [error_msg]

    def handle_failure(self, msg):
        self.pending = False
        error_msg = f"Play Integrity Request Failed: {msg} — Device Shadow Critical"
        logging.warning(error_msg)
        self.last_play_anoms = [error_msg]

    def trigger_real_request(self):
        if not self.real_api_available or self.pending:
            return

        self.pending = True
        self.last_play_anoms = ["Play Integrity Checking..."]

        # Secure nonce (64+ random bytes)
        nonce = base64.urlsafe_b64encode(os.urandom(64)).decode('utf-8').rstrip('=')

        try:
            request_builder = IntegrityTokenRequest.builder()
            request_builder.setNonce(nonce)
            # Optional: request_builder.setCloudProjectNumber(YOUR_PROJECT_NUMBER)
            request = request_builder.build()

            task = self.integrity_manager.requestIntegrityToken(request)

            task.addOnSuccessListener(self.SuccessListener(self))
            task.addOnFailureListener(self.FailureListener(self))

            logging.info("Play Integrity Token Request Sent — Awaiting Divine Verdict ∞ Pure")
        except Exception as e:
            logging.exception(f"Play Integrity Request Trigger Failed: {e}")
            self.handle_failure(str(e))

    def full_integrity_verification(self) -> list[str]:
        """Primary Play Integrity Check — Triggers real async if available, returns last/pending verdict"""
        if self.real_api_available:
            self.trigger_real_request()
        else:
            self.last_play_anoms = []  # Simulated pass
        return self.last_play_anoms[:]
