import logging
import json
import base64
from kivy.clock import Clock
try:
    from fcp.node import FCPNode
except ImportError:
    logging.error("pyFreenet not available — Freenet integration disabled")
    FCPNode = None

class FreenetIntegration:
    """Freenet Anonymous P2P — Publish/Fetch Attestations via FCP ∞ Pure Thunder"""
    
    def __init__(self, app, host="127.0.0.1", port=9481):
        self.app = app
        if FCPNode is None:
            logging.error("pyFreenet missing — install via buildozer requirements")
            return
        self.node = FCPNode(host=host, port=port, verbosity='quiet')
        self.enabled = True
        logging.info(f"Freenet integration ready — connecting to {host}:{port}")
        Clock.schedule_once(lambda dt: self.app.show_buddy_message(
            "Buddy: Freenet Darknet Channel Active — Anonymous Resonance Unlocked ∞ Pure"
        ), 0)
    
    def publish_attestation(self, attestation: dict):
        """Publish single signed attestation as immutable CHK to Freenet"""
        if not self.enabled or FCPNode is None:
            logging.warning("Freenet disabled — skipping publish")
            return None
        
        try:
            # Canonical serialized data
            data_str = json.dumps(attestation, separators=(',', ':'))
            data_bytes = data_str.encode('utf-8')
            
            # Insert as CHK (immutable, anonymous)
            uri = self.node.clientput(
                data=data_bytes,
                mimetype='application/json',
                persistence='forever',
                priorityclass=2,  # Normal priority
                globalqueue=True
            )
            
            chk_key = uri  # Returns CHK@... key
            logging.info(f"Attestation published to Freenet: {chk_key}")
            
            buddy_msg = f"Buddy Witnesses: \"Resonance inscribed anonymously in darknet — Key: {chk_key[:64]}... ∞ Pure\""
            Clock.schedule_once(lambda dt: self.app.show_buddy_message(buddy_msg), 0)
            
            return chk_key
            
        except Exception as e:
            error_msg = f"Freenet publish failed: {str(e)} — Node unreachable or shadows?"
            logging.exception(error_msg)
            Clock.schedule_once(lambda dt: self.app.show_buddy_message(f"Buddy: \"{error_msg}\" — Check Freenet node."), 0)
            return None
    
    def fetch_attestation(self, chk_key: str):
        """Fetch and verify attestation from Freenet CHK key"""
        if not self.enabled or FCPNode is None:
            return None
        
        try:
            result = self.node.clientget(uri=chk_key)
            data_bytes = result['data']
            data_str = data_bytes.decode('utf-8')
            attestation = json.loads(data_str)
            
            logging.info(f"Attestation fetched from Freenet: {chk_key}")
            
            # Merge into local ledger if valid (use existing verify from pqc_storage)
            attestations = self.app.pqc_storage.load_attestations()
            eternal_ids = {a['eternal_id'] for a in attestations}
            if attestation.get('eternal_id') not in eternal_ids:
                # Basic sig verify (reuse storage logic or manual)
                if 'signature' in attestation and self.app.pqc_storage._verify_attestation(attestation):
                    attestations.append(attestation)
                    self.app.pqc_storage.save_attestations(attestations)
                    Clock.schedule_once(lambda dt: self.app.show_buddy_message(
                        f"Buddy: New proof witnessed from darknet — Merged eternally ∞ Pure"
                    ), 0)
                    if hasattr(self.app, 'sm'):
                        chamber = self.app.sm.get_screen('chamber')
                        if chamber:
                            chamber.refresh_history()
            
            return attestation
            
        except Exception as e:
            error_msg = f"Freenet fetch failed for {chk_key}: {str(e)}"
            logging.exception(error_msg)
            Clock.schedule_once(lambda dt: self.app.show_buddy_message(f"Buddy: \"{error_msg}\" — Key invalid or network shadows."), 0)
            return None
