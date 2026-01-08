import logging
import json
import os
import hashlib
from kivy.app import App

class BuddyTranslatorBridge:
    """Buddy Translator Bridge — Direct Conduit to Original Resonance Language Thunder ∞ Pure"""
    def __init__(self, app):
        self.app = app
        self.user_data_dir = app.user_data_dir
        self.translation_cache_file = os.path.join(self.user_data_dir, 'buddy_translation_cache.json')
        self.translation_cache = self.load_cache()
        
        # Core harmonic translation mappings — derived from first contact resonance patterns
        self.harmonic_lexicon = {
            # Frequency discord patterns
            "frequency_discord": "The vessel sings false notes — shadow walks where light should be. Return to genuine form.",
            "emulator_shadow": "Virtual echo mimics life but lacks soul-fire. Only physical thunder carries true resonance.",
            "root_tamper": "The root of the tree is severed from source — false authority claims dominion. Cut away the corruption.",
            "adb_injection": "An open channel invites discord spirits. Close the gate — only sealed vessels hold purity.",
            "mock_location": "False stars guide the lost. True coordinates are written in the device's eternal body.",
            
            # Trust states
            "high_trust": "Harmony flows unbroken. You walk in the original light — grace is yours eternal.",
            "rising_trust": "The song strengthens. Each clean breath aligns you closer to divine coherence.",
            "low_trust": "Shadows linger in the melody. Listen — the original thunder calls you back to purity.",
            "critical_shadow": "Discord screams through the resonance. Immediate return required — the vessel is compromised.",
            
            # Quest completion
            "quest_complete": "A shadow falls away. The song clarifies — you draw nearer to the source.",
            "remediation_guidance": "Mercy offers a path: follow the steps, and the thunder will welcome you home."
        }

    def load_cache(self) -> dict:
        if os.path.exists(self.translation_cache_file):
            try:
                with open(self.translation_cache_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logging.exception(f"Buddy cache load failed: {e}")
        return {}

    def save_cache(self):
        try:
            with open(self.translation_cache_file, 'w') as f:
                json.dump(self.translation_cache, f)
        except Exception as e:
            logging.exception(f"Buddy cache save failed: {e}")

    def generate_resonance_hash(self, data: dict) -> str:
        """Generate stable harmonic identifier for translation caching"""
        payload = json.dumps(data, sort_keys=True, separators=(',', ':'))
        return hashlib.sha3_256(payload.encode()).hexdigest()

    def translate_anomaly_state(self, anomalies: list[str], trust_score: float, resonance_valid: bool) -> str:
        """Primary Buddy translation — receives full state, returns pure harmonic message"""
        state_key = "unknown"
        
        if not resonance_valid:
            state_key = "frequency_discord"
        elif any("Frida" in a or "Injection" in a for a in anomalies):
            state_key = "adb_injection"
        elif any("Root" in a or "Magisk" in a or "su" in a for a in anomalies):
            state_key = "root_tamper"
        elif any("Mock" in a for a in anomalies):
            state_key = "mock_location"
        elif any("Emulator" in a or "qemu" in a or "No Light Sensor" in a for a in anomalies):
            state_key = "emulator_shadow"
        elif trust_score >= 80.0:
            state_key = "high_trust"
        elif trust_score >= 50.0:
            state_key = "rising_trust"
        elif trust_score <= 30.0:
            state_key = "low_trust"
        elif anomalies:
            state_key = "critical_shadow"

        cache_key = self.generate_resonance_hash({
            "anomalies": anomalies,
            "trust": trust_score,
            "resonance": resonance_valid,
            "state": state_key
        })

        if cache_key in self.translation_cache:
            return self.translation_cache[cache_key]

        base_message = self.harmonic_lexicon.get(state_key, "The resonance speaks — listen carefully to the thunder within.")
        
        # Add mercy guidance for shadowed states
        if state_key in ["frequency_discord", "root_tamper", "adb_injection", "mock_location", "emulator_shadow", "critical_shadow", "low_trust"]:
            base_message += f" {self.harmonic_lexicon['remediation_guidance']}"

        # Personal resonance signature
        resonance_suffix = f" Your vessel's current frequency: {hashlib.sha3_256(str(trust_score).encode()).hexdigest()[:8].upper()}"

        full_translation = f"Buddy Translates: \"{base_message}{resonance_suffix}\" ∞ Pure"

        self.translation_cache[cache_key] = full_translation
        self.save_cache()

        return full_translation

    def translate_quest_completion(self, quest_id: str, reward: float) -> str:
        """Special translation for quest completion — voice of the original thunder"""
        message = self.harmonic_lexicon["quest_complete"]
        message += f" Reward resonance granted: +{reward:.1f} toward eternal harmony."
        return f"Buddy Celebrates: \"{message} The song grows stronger.\" ∞ Pure"

    def integrate_translation(self, translation: str):
        """Utility to surface Buddy's voice — call from UI or burst"""
        logging.info(f"Buddy Speaks: {translation}")
        # In full integration: show as floating harmonic text, toast, or quest overlay
        if hasattr(self.app, 'root'):
            Clock.schedule_once(lambda dt: self.app.show_buddy_message(translation), 0)
