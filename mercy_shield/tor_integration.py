import logging
import socket
import socks  # PySocks
from kivy.clock import Clock

class TorIntegration:
    """Tor Anonymity Integration — SOCKS5h Proxy via Orbot ∞ Pure Thunder"""
    
    def __init__(self, app, proxy_host="127.0.0.1", proxy_port=9050):
        self.app = app
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.enabled = False
        self.original_socket = socket.socket
        logging.info("Tor integration ready — awaiting Orbot proxy")
    
    def enable_tor(self):
        """Enable Tor proxy — monkey patch sockets for all outgoing traffic"""
        if self.enabled:
            return True
        
        try:
            # SOCKS5h for remote DNS resolve (onion support)
            socks.setdefaultproxy(
                proxy_type=socks.PROXY_TYPE_SOCKS5,
                addr=self.proxy_host,
                port=self.proxy_port,
                rdns=True  # Remote DNS
            )
            socket.socket = socks.socksocket
            
            # Test connection (optional simple check)
            test_sock = socks.socksocket()
            test_sock.settimeout(10)
            test_sock.connect(("check.torproject.org", 80))
            test_sock.close()
            
            self.enabled = True
            logging.info("Tor proxy enabled — anonymity sealed")
            Clock.schedule_once(lambda dt: self.app.show_buddy_message(
                "Buddy: Tor Anonymity Active — All connections hidden in onion layers ∞ Pure Thunder"
            ), 0)
            return True
            
        except Exception as e:
            error_msg = f"Tor enable failed: {str(e)} — Orbot running? App selected?"
            logging.exception(error_msg)
            Clock.schedule_once(lambda dt: self.app.show_buddy_message(
                f"Buddy: \"{error_msg}\" — Install/start Orbot and try again."
            ), 0)
            return False
    
    def disable_tor(self):
        """Disable Tor proxy — restore normal sockets"""
        if not self.enabled:
            return
        
        socket.socket = self.original_socket
        socks.setdefaultproxy()  # Clear
        self.enabled = False
        logging.info("Tor proxy disabled")
        Clock.schedule_once(lambda dt: self.app.show_buddy_message(
            "Buddy: Tor Anonymity Disabled — Direct resonance restored"
        ), 0)
    
    def is_enabled(self):
        return self.enabled
