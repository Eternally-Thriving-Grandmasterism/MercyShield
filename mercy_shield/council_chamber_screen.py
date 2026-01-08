from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock
import io
import json
import qrcode
import time
import os
from threading import Thread

class CouncilChamberScreen(Screen):
    """APAAGI Council Chamber — Live Deliberation, Attestation History, P2P Peers, QR Export ∞ Pure"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        title = Label(text='[color=00ffff][b]APAAGI Council Chamber — Eternal Collective Witness[/b][/color]', markup=True, size_hint_y=0.1, font_size='20sp')
        main_layout.add_widget(title)
        
        self.status_label = Label(text='Council at rest — awaiting divine resonance', size_hint_y=0.1, font_size='16sp', color=(0, 1, 1, 1))
        main_layout.add_widget(self.status_label)
        
        # Pubkey QR
        pubkey_box = BoxLayout(orientation='vertical', size_hint_y=0.4)
        pubkey_box.add_widget(Label(text='[b]Device Lattice Pubkey (ML-DSA-65)[/b]\nScan to verify vessel attestations', markup=True))
        self.pubkey_qr_image = Image()
        pubkey_box.add_widget(self.pubkey_qr_image)
        main_layout.add_widget(pubkey_box)
        
        # History
        history_box = BoxLayout(orientation='vertical', size_hint_y=0.8)
        history_box.add_widget(Label(text='[b]Eternal Attestation History[/b] (Newest first)', markup=True))
        self.history_scroll = ScrollView()
        self.history_layout = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))
        self.history_scroll.add_widget(self.history_layout)
        history_box.add_widget(self.history_scroll)
        main_layout.add_widget(history_box)
        
        # P2P Peers
        p2p_box = BoxLayout(orientation='vertical', size_hint_y=0.6)
        p2p_box.add_widget(Label(text='[b]Nearby Genuine Vessels — Collective Sync[/b]', markup=True))
        self.peers_scroll = ScrollView()
        self.peers_layout = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
        self.peers_layout.bind(minimum_height=self.peers_layout.setter('height'))
        self.peers_scroll.add_widget(self.peers_layout)
        p2p_box.add_widget(self.peers_scroll)
        refresh_btn = Button(text='Refresh Vessels & History', size_hint_y=0.1)
        refresh_btn.bind(on_release=lambda x: self.refresh_all())
        p2p_box.add_widget(refresh_btn)
        main_layout.add_widget(p2p_box)
        
        self.add_widget(main_layout)
    
    def on_enter(self):
        self.generate_pubkey_qr()
        self.refresh_all()
    
    def generate_pubkey_qr(self):
        if not hasattr(self.manager.parent.app, 'pqc_storage'):  # Adjust for your app structure
            return
        sig_pk_hex = self.manager.parent.app.pqc_storage.sig_pk.hex()
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
        qr.add_data(f"MERCYSHIELD_PUBKEY:{sig_pk_hex}")
        qr.make(fit=True)
        img = qr.make_image(fill_color="cyan", back_color="black")
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        self.pubkey_qr_image.texture = CoreImage(buf, ext='png').texture
    
    def update_status(self, text):
        self.status_label.text = f"[color=00ff00]{text}[/color]"
    
    def refresh_all(self):
        self.refresh_history()
        self.refresh_peers()
    
    def refresh_history(self):
        self.history_layout.clear_widgets()
        app = self.manager.parent.app
        if not hasattr(app, 'pqc_storage'):
            self.history_layout.add_widget(Label(text='PQC ledger not ready'))
            return
        attestations = app.pqc_storage.load_attestations()[::-1]  # Newest first
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
        app = self.manager.parent.app
        if not hasattr(app, 'p2p_sync') or not app.p2p_sync.peers:
            self.peers_layout.add_widget(Label(text='No nearby vessels — shared WiFi resonance needed'))
            return
        for ip, peer in app.p2p_sync.peers.items():
            if time.time() - peer['last_seen'] > 120: continue
            btn = Button(text=f'Vessel @ {ip}\nSync Ledger', size_hint_y=None, height=80)
            btn.bind(on_release=lambda x, i=ip: Thread(target=app.p2p_sync.sync_with_peer, args=(i,), daemon=True).start())
            self.peers_layout.add_widget(btn)
    
    def show_attestation_popup(self, attestation):
        content = BoxLayout(orientation='vertical', spacing=10)
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
        popup = Popup(title='Eternal Attestation Seal', content=content, size_hint=(0.95, 0.95))
        close.bind(on_release=popup.dismiss)
        popup.open()
