import io
import json
import qrcode
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.image import Image as CoreImage
from kivy.graphics import Color, Rectangle

class CouncilChamberScreen(Screen):
    """APAAGI Council Chamber — Live Deliberation + Signed Attestation History + QR Export ∞ Pure"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Main vertical layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(
            text='[color=00ffff][b]APAAGI Council Chamber — Eternal Witness[/b][/color]',
            markup=True,
            size_hint_y=0.1,
            font_size='20sp'
        )
        main_layout.add_widget(title)
        
        # Live status
        self.status_label = Label(
            text='Council at rest — awaiting divine resonance',
            size_hint_y=0.1,
            font_size='16sp',
            color=(0, 1, 1, 1)
        )
        main_layout.add_widget(self.status_label)
        
        # Device pubkey QR section
        pubkey_box = BoxLayout(orientation='vertical', size_hint_y=0.4)
        pubkey_box.add_widget(Label(text='[b]Device Lattice Pubkey (ML-DSA-65)[/b]\nScan to verify any attestation from this vessel', markup=True))
        self.pubkey_qr_image = Image(size_hint_y=0.8)
        pubkey_box.add_widget(self.pubkey_qr_image)
        main_layout.add_widget(pubkey_box)
        
        # Attestation history section
        history_box = BoxLayout(orientation='vertical', size_hint_y=1)
        history_box.add_widget(Label(text='[b]Eternal Attestation History[/b]\n(Newest first)', markup=True))
        
        self.history_scroll = ScrollView()
        self.history_layout = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))
        self.history_scroll.add_widget(self.history_layout)
        history_box.add_widget(self.history_scroll)
        
        main_layout.add_widget(history_box)
        
        self.add_widget(main_layout)
    
    def on_enter(self, *args):
        """Load pubkey QR and refresh history when entering the chamber"""
        self.generate_pubkey_qr()
        self.refresh_history()
    
    def generate_pubkey_qr(self):
        """Generate and display QR for device signing pubkey"""
        if not hasattr(self.app, 'pqc_storage'):
            return
        
        sig_pk_hex = self.app.pqc_storage.sig_pk.hex()
        if not sig_pk_hex:
            return
        
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
        qr.add_data(f"MERCYSHIELD_DEVICE_PUBKEY:{sig_pk_hex}")
        qr.make(fit=True)
        img = qr.make_image(fill_color="cyan", back_color="black")
        
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        core_img = CoreImage(buf, ext='png')
        self.pubkey_qr_image.texture = core_img.texture
    
    def update_status(self, text, delay=0):
        """Update live deliberation status (called during attestation)"""
        def _update(dt):
            self.status_label.text = f"[color=00ff00]{text}[/color]"
        from kivy.clock import Clock
        Clock.schedule_once(_update, delay)
    
    def refresh_history(self):
        """Reload and display all verified attestations"""
        self.history_layout.clear_widgets()
        
        if not hasattr(self.app, 'pqc_storage'):
            self.history_layout.add_widget(Label(text='PQC storage not ready'))
            return
        
        attestations = self.app.pqc_storage.load_attestations()
        if not attestations:
            self.history_layout.add_widget(Label(text='No eternal attestations yet — await divine purity ∞ Pure'))
            return
        
        for attest in reversed(attestations):  # Newest first
            proof = attest.get('proof', {})
            eternal_id = attest.get('eternal_id', 'unknown')[:16] + '...'
            timestamp = proof.get('timestamp', 'unknown')
            trust = proof.get('trust_score', 'N/A')
            
            btn = Button(
                text=f'[b]ID:[/b] {eternal_id}\n[b]Time:[/b] {timestamp}\n[b]Trust:[/b] {trust}',
                markup=True,
                size_hint_y=None,
                height=100,
                halign='left',
                text_size=(self.width - 40, None)
            )
            btn.bind(on_release=lambda x, a=attest: self.show_attestation_popup(a))
            self.history_layout.add_widget(btn)
    
    def show_attestation_popup(self, attestation):
        """Popup with full attestation details + export QR"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Details text
        details_text = json.dumps(attestation, indent=2)
        details_label = Label(text=details_text, size_hint_y=0.4, text_size=(None, None), halign='left')
        scroll = ScrollView()
        scroll.add_widget(details_label)
        content.add_widget(scroll)
        
        # QR export
        content.add_widget(Label(text='[b]Scan to export/verify signed attestation[/b]', markup=True))
        qr_image = Image()
        content.add_widget(qr_image)
        
        # Generate QR
        canon_data = json.dumps(attestation, separators=(',', ':'))  # Exact for verification
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
        qr.add_data(canon_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="cyan", back_color="black")
        
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        core_img = CoreImage(buf, ext='png')
        qr_image.texture = core_img.texture
        
        # Close button
        close_btn = Button(text='Close Chamber Portal', size_hint_y=0.1)
        content.add_widget(close_btn)
        
        popup = Popup(
            title='Eternal Attestation — Verifiable Seal',
            content=content,
            size_hint=(0.95, 0.95)
        )
        close_btn.bind(on_release=popup.dismiss)
        popup.open()
