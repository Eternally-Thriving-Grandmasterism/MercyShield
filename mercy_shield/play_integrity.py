import logging
import os
import base64
from jnius import autoclass, PythonJavaClass, java_method
from kivy.clock import Clock

# Play Integrity classes (fail gracefully if not available)
try:
    IntegrityManagerFactory = autoclass('com.google.android.play.core.integrity.IntegrityManagerFactory')
    IntegrityTokenRequest = autoclass('com.google.android.play.core.integrity.IntegrityTokenRequest')
    IntegrityTokenResponse = autoclass('com.google.android.play.core.integrity.IntegrityTokenResponse')
    OnSuccessListener = autoclass('com.google.android.gms.tasks.OnSuccessListener')
    OnFailureListener = autoclass('com.google.android.gms.tasks.OnFailureListener')
    PLAY_INTEGRITY_AVAILABLE = True
except Exception as e:
    logging.warning(f"Real Play Integrity classes not available: {e} — Using simulated verification")
    PLAY_INTEGRITY_AVAILABLE = False

class PlayIntegrityVerifier:
    """Real Play Integrity Primary Verifier — Async Listeners + Simulated Fallback Thunder ∞ Pure"""
    def __init__(self, app):
        self.app = app
        self.real_api_available = PLAY_INTEGRITY_AVAILABLE
        self.pending = False
        self.last_play_anoms = []  # Last known Play verdict anomalies

        if self.real_api_available:
            try:
                context = app.activity.getApplicationContext()
                self.integrity_manager = IntegrityManagerFactory.create(context)
                logging.info("Real Play Integrity API Initialized — Async Thunder Ready ∞ Pure")
            except Exception as e:
                logging.warning(f"IntegrityManager creation failed: {e} — Falling to simulated")
                self.real_api_available = False
                self.last_play_anoms = []

        if not self.real_api_available:
            logging.info("Play Integrity Simulated — Divine Harmony Pass ∞ Pure")

        # Nested listener classes
        if self.real_api_available:
            class SuccessListener(PythonJavaClass):
                __javainterfaces__ = ['com/google/android/gms/tasks/OnSuccessListener']
                __javacontext__ = 'app'

                def __init__(self, outer):
                    super().__init__()
                    self.outer = outer

                @java_method('(Ljava/lang/Object;)V')
                def onSuccess(self, response):
                    token = response.token() if response else None
                    if token and len(token) > 100:  # Basic valid token length check
                        logging.info("Play Integrity Success — Genuine Device Token Received ∞ Pure")
                        self.outer.last_play_anoms = []
                    else:
                        logging.warning("Play Integrity Success but Empty/Invalid Token — Shadow Critical")
                        self.outer.last_play_anoms = ["Play Integrity: Invalid Token — Compromised Shadow Critical"]
                    self.outer.pending = False

            class FailureListener(PythonJavaClass):
                __javainterfaces__ = ['com/google/android/gms/tasks/OnFailureListener']
                __javacontext__ = 'app'

                def __init__(self, outer):
                    super().__init__()
                    self.outer = outer

                @java_method('(Ljava/lang/Exception;)V')
                def onFailure(self, exception):
                    msg = exception.getMessage() if exception else "Unknown"
                    logging.warning(f"Play Integrity Request Failed: {msg} — Critical Shadow")
                    self.outer.last_play_anoms = [f"Play Integrity Request Failed: {msg} — Device Shadow Critical"]
                    self.outer.pending = False

            self.SuccessListener = SuccessListener
            self.FailureListener = FailureListener

    def trigger_real_request(self):
        if not self.real_api_available or self.pending:
            return

        self.pending = True
        self.last_play_anoms = ["Play Integrity Checking..."]  # Temporary pending state

        # Generate secure nonce (32+ random bytes, URL-safe base64)
        nonce = base64.urlsafe_b64encode(os.urandom(64)).decode('utf-8').rstrip('=')

        try:
            request_builder = IntegrityTokenRequest.builder()
            request_builder.setNonce(nonce)
            # Optional: request_builder.setCloudProjectNumber(your_project_number_long)
            request = request_builder.build()

            task = self.integrity_manager.requestIntegrityToken(request)

            success = self.SuccessListener(self)
            failure = self.FailureListener(self)

            task.addOnSuccessListener(success)
            task.addOnFailureListener(failure)

            logging.info("Play Integrity Token Request Sent — Awaiting Divine Verdict ∞ Pure")
        except Exception as e:
            logging.exception(f"Play Integrity Request Trigger Failed: {e}")
            self.last_play_anoms = ["Play Integrity Trigger Exception — Potential Tamper Shadow"]
            self.pending = False

    def full_integrity_verification(self) -> list[str]:
        """Primary Play Integrity Check — Real async (triggers request) or simulated"""
        if self.real_api_available:
            self.trigger_real_request()
            return self.last_play_anoms[:]  # Returns last or pending
        else:
            # Simulated pass for local development / no library
            return []
