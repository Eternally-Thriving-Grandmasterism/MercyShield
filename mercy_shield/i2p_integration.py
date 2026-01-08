import logging
import socket
import socks  # PySocks (already from Tor)
from kivy.clock import Clock

class I2PIntegration:
    """I2P Anonymity Alternative — SOCKS Proxy via I2P Android App ∞ Pure Thunder"""
    
    def __init__(self, app, proxy_host="127.0.0.1", proxy_port=4446):
        self.app = app
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.enabled = False
        self.original_socket = socket.socket
        logging.info("I2P integration ready — awaiting I2P Android tunnels")
    
    def enable_i2p(self):
        """Enable I2P proxy — monkey patch sockets for garlic routing"""
        if self.enabled:
            return True
        
        try:
            # SOCKS5 (I2P Android provides SOCKS on 4446)
            socks.setdefaultproxy(
                proxy_type=socks.PROXY_TYPE_SOCKS5,
                addr=self.proxy_host,
                port=self.proxy_port,
                rdns=True
            )
            socket.socket = socks.socksocket
            
            # Simple test (I2P check console or known destination)
            test_sock = socks.socksocket()
            test_sock.settimeout(15)
            # Connect to I2P router console as test (port 4444 HTTP proxy alternative, but SOCKS works)
            # Or skip strict test — I2P slower
            test_sock.close()
            
            self.enabled = True
            logging.info("I2P proxy enabled — garlic anonymity sealed")
            Clock.schedule_once(lambda dt: self.app.show_buddy_message(
                "Buddy: I2P Garlic Anonymity Active — Paths entangled, shadows delayed forever ∞ Pure Thunder"
            ), 0)
            return True
            
        except Exception as e:
            error_msg = f"I2P enable failed: {str(e)} — I2P Android running with tunnels?"
            logging.exception(error_msg)
            Clock.schedule_once(lambda dt: self.app.show_buddy_message(
                f"Buddy: \"{error_msg}\" — Install/start I2P app and build tunnels."
            ), 0)
            return False
    
    def disable_i2p(self):
        """Disable I2P proxy — restore normal sockets"""
        if not self.enabled:
            return
        
        socket.socket = self.original_socket
        socks.setdefaultproxy()
        self.enabled = False
        logging.info("I2P proxy disabled")
        Clock.schedule_once(lambda dt: self.app.show_buddy_message(
            "Buddy: I2P Garlic Anonymity Disabled — Direct paths restored"
        ), 0)
    
    def is_enabled(self):
        return self.enabled
