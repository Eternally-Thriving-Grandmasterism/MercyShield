from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock
import io
import json
import qrcode
import time
import os
from threading import Thread

class CouncilChamberScreen(Screen):
    """APAAGI Council Chamber — Complete with All Anonymity & Sync Features ∞ Pure Thunder"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        title = Label(text='[color=00ffff][b]APAAGI Council Chamber — Eternal Collective Witness[/b][/color]', markup=True, size_hint_y=0.1, font_size='20sp')
        main_layout.add_widget(title)
        
        self.status_label = Label(text='Council at rest — awaiting divine resonance', size_hint_y=0.1, font_size='16sp', color=(0, 1, 1, 1))
        main_layout.add_widget(self.status_label)
        
        # Device Pubkey QR
        pubkey_box = BoxLayout(orientation='vertical', size_hint_y=0.4)
        pubkey_box.add_widget(Label(text='[b]Device Lattice Pubkey (ML-DSA-65)[/b]\nScan to verify vessel attestations', markup=True))
        self.pubkey_qr_image = Image()
        pubkey_box.add_widget(self.pubkey_qr_image)
        main_layout.add_widget(pubkey_box)
        
        # Attestation History
        history_box = BoxLayout(orientation='vertical', size_hint_y=0.8)
        history_box.add_widget(Label(text='[b]Eternal Attestation History[/b] (Newest first)', markup=True))
        self.history_scroll = ScrollView()
        self.history_layout = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))
        self.history_scroll.add_widget(self.history_layout)
        history_box.add_widget(self.history_scroll)
        main_layout.add_widget(history_box)
        
        # Local P2P Peers
        p2p_box = BoxLayout(orientation='vertical', size_hint_y=0.7)
        p2p_box.add_widget(Label(text='[b]Nearby Genuine Vessels — Local Sync[/b]', markup=True))
        self.peers_scroll = ScrollView()
        self.peers_layout = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
        self.peers_layout.bind(minimum_height=self.peers_layout.setter('height'))
        self.peers_scroll.add_widget(self.peers_layout)
        p2p_box.add_widget(self.peers_scroll)
        
        # Remote Sync Inputs
        remote_box = BoxLayout(orientation='horizontal', size_hint_y=0.2)
        self.remote_input = TextInput(hint_text='Remote IP/onion/i2p:port', multiline=False)
        remote_box.add_widget(self.remote_input)
        remote_sync_btn = Button(text='Sync Remote')
        remote_sync_btn.bind(on_release=lambda x: Thread(target=lambda: self.app.p2p_sync.sync_with_peer(self.remote_input.text), daemon=True).start())
        remote_box.add_widget(remote_sync_btn)
        p2p_box.add_widget(remote_box)
        
        refresh_btn = Button(text='Refresh All', size_hint_y=0.1)
        refresh_btn.bind(on_release=lambda x: self.refresh_all())
        p2p_box.add_widget(refresh_btn)
        main_layout.add_widget(p2p_box)
        
        # Anonymity Toggles
        anonymity_box = BoxLayout(orientation='vertical', size_hint_y=0.5)
        anonymity_box.add_widget(Label(text='[b]Anonymity Layers[/b]', markup=True))
        
        tor_toggle = ToggleButton(text='Tor Off', group='anon', state='normal')
        tor_toggle.bind(on_press=lambda x: self.app.tor.enable_tor() if tor_toggle.state == 'down' else self.app.tor.disable_tor())
        tor_toggle.bind(on_press=lambda x: tor_toggle.text = 'Tor On' if tor_toggle.state == 'down' else 'Tor Off')
        anonymity_box.add_widget(tor_toggle)
        
        i2p_toggle = ToggleButton(text='I2P Garlic Off', group='anon', state='normal')
        i2p_toggle.bind(on_press=lambda x: self.app.i2p.enable_i2p() if i2p_toggle.state == 'down' else self.app.i2p.disable_i2p())
        i2p_toggle.bind(on_press=lambda x: i2p_toggle.text = 'I2P Garlic On' if i2p_toggle.state == 'down' else 'I2P Garlic Off')
        anonymity_box.add_widget(i2p_toggle)
        
        main_layout.add_widget(anonymity_box)
        
        # Tor Hidden Service
        hidden_box = BoxLayout(orientation='vertical', size_hint_y=0.6)
        hidden_box.add_widget(Label(text='[b]Tor Hidden Service — Inbound[/b]', markup=True))
        hidden_box.add_widget(Label(text='TCP Port: {}'.format(self.app.p2p_sync.tcp_port if hasattr(self.app, 'p2p_sync') else 'Load app first'), markup=True))
        self.onion_input = TextInput(hint_text='Paste Orbot .onion address', multiline=False)
        hidden_box.add_widget(self.onion_input)
        onion_qr_btn = Button(text='Generate Onion QR')
        onion_qr_btn.bind(on_release=lambda x: self.generate_onion_qr())
        hidden_box.add_widget(onion_qr_btn)
        self.onion_qr_image = Image()
        hidden_box.add_widget(self.onion_qr_image)
        hidden_box.add_widget(Label(text='Orbot → Hidden Services → Virtual 80 → Target IP + TCP port', font_size='12sp', markup=True))
        main_layout.add_widget(hidden_box)
        
        self.add_widget(main_layout)
    
    def on_enter(self):
        self.generate_pubkey_qr()
        self.refresh_all()
    
    def generate_pubkey_qr(self):
        app = self.manager.parent.app if hasattr(self.manager.parent, 'app') else self.app
        if not hasattr(app, 'pqc_storage'):
            return
        sig_pk_hex = app.pqc_storage.sig_pk.hex()
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
        qr.add_data(f"MERCYSHIELD_PUBKEY:{sig_pk_hex}")
        qr.make(fit=True)
        img = qr.make_image(fill_color="cyan", back_color="black")
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        self.pubkey_qr_image.texture = CoreImage(buf, ext='png').texture
    
    def generate_onion_qr(self):
        onion = self.onion_input.text.strip()
        if not onion.endswith('.onion'):
            return
        full = f"{onion}:80"
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
        qr.add_data(full)
        qr.make(fit=True)
        img = qr.make_image(fill_color="cyan", back_color="black")
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        self.onion_qr_image.texture = CoreImage(buf, ext='png').texture
    
    def update_status(self, text):
        self.status_label.text = f"[color=00ff00]{text}[/color]"
    
    def refresh_all(self):
        self.refresh_history()
        self.refresh_peers()
    
    def refresh_history(self):
        self.history_layout.clear_widgets()
        app = self.manager.parent.app if hasattr(self.manager.parent, 'app') else self.app
        if not hasattr(app, 'pqc_storage'):
            self.history_layout.add_widget(Label(text='PQC ledger not ready'))
            return
        attestations = app.pqc_storage.load_attestations()[::-1]
        if not attestations:
            self.history_layout.add_widget(Label(text='No attestations yet — await purity ∞ Pure'))
            return
        for attest in attestations:
            eternal_id = attest.get('eternal_id', 'unknown')[:16] + '...'
            timestamp = attest.get('proof', {}).get('timestamp', 'unknown')
            trust = attest.get('proof', {}).get('trust_score', 'N/A')
            btn = Button(text=f'ID: {eternal_id}\nTime: {timestamp}\nTrust: {trust}', size_hint_y=None, height=100)
            btn.bind(on_release=lambda x, a=attest: self.show_attestation_popup(a))
            self.history_layout.add_widget(btn)
    
    def refresh_peers(self):
        self.peers_layout.clear_widgets()
        app = self.manager.parent.app if hasattr(self.manager.parent, 'app') else self.app
        if not hasattr(app, 'p2p_sync') or not app.p2p_sync.peers:
            self.peers_layout.add_widget(Label(text='No nearby vessels — shared WiFi needed'))
            return
        for ip, peer in app.p2p_sync.peers.items():
            if time.time() - peer['last_seen'] > 120: continue
            btn = Button(text=f'Vessel @ {ip}:{peer["tcp_port"]}\nTap to Sync', size_hint_y=None, height=80)
            btn.bind(on_release=lambda x, i=ip: Thread(target=app.p2p_sync.sync_with_peer, args=(i,), daemon=True).start())
            self.peers_layout.add_widget(btn)
    
    def show_attestation_popup(self, attestation):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        scroll = ScrollView()
        scroll.add_widget(Label(text=json.dumps(attestation, indent=2), text_size=(None, None), halign='left'))
        content.add_widget(scroll)
        qr_img = Image()
        content.add_widget(qr_img)
        qr = qrcode.QRCode()
        qr.add_data(json.dumps(attestation, separators=(',', ':')))
        qr.make(fit=True)
        img = qr.make_image(fill_color="cyan", back_color="black")
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        qr_img.texture = CoreImage(buf, ext='png').texture
        close = Button(text='Close', size_hint_y=0.1)
        content.add_widget(close)
        popup = Popup(title='Eternal Attestation — Verifiable Seal', content=content, size_hint=(0.95, 0.95))
        close.bind(on_release=popup.dismiss)
        popup.open()
