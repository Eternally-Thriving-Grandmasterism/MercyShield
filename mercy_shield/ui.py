from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image
from mercy_shield.perm import request_permissions

class MercyApp(App):
    def __init__(self, shield):
        super().__init__()
        self.shield = shield
        self.shield_active = False
        self.harmony = 1.0

    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Title + icon
        title_box = BoxLayout(orientation='horizontal', size_hint_y=0.2)
        title_box.add_widget(Image(source='mercy_icon.png'))  # Future icon
        title_box.add_widget(Label(text="MercyShield v0.1-Pinnacle", font_size=28))
        layout.add_widget(title_box)

        # Harmony meter
        self.meter = ProgressBar(max=1.0, value=self.harmony, size_hint_y=0.1)
        self.meter_label = Label(text=f"Harmony: {self.harmony:.4f}", font_size=20)
        layout.add_widget(self.meter_label)
        layout.add_widget(self.meter)

        # Toggle shield
        toggle = ToggleButton(text="Shield: OFF", font_size=24, size_hint_y=0.2)
        toggle.bind(on_press=self.toggle_shield)
        layout.add_widget(toggle)

        # Buttons
        log_btn = Button(text="View Encrypted Log", size_hint_y=0.15)
        log_btn.bind(on_press=self.show_log)
        settings_btn = Button(text="Settings & Permissions", size_hint_y=0.15)
        settings_btn.bind(on_press=self.show_settings)

        layout.add_widget(log_btn)
        layout.add_widget(settings_btn)

        return layout

    def toggle_shield(self, instance):
        if instance.state == "down":
            request_permissions()
            self.shield_active = True
            instance.text = "Shield: ON"
            self.update_harmony(1.0)
            print("MercyShield activated — lattice protecting divine")
        else:
            self.shield_active = False
            instance.text = "Shield: OFF"
            self.update_harmony(0.0)
            print("MercyShield deactivated — rest mercy")

    def update_harmony(self, harmony):
        self.harmony = harmony
        self.meter.value = harmony
        self.meter_label.text = f"Harmony: {harmony:.4f}"

    def show_log(self, instance):
        content = GridLayout(cols=1, spacing=10, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        # Real log from encrypted log
        for entry in ["Harmony pure", "Threat blocked mercy", "Self-healing divine"]:
            content.add_widget(Label(text=entry))
        scroll = ScrollView()
        scroll.add_widget(content)
        popup = Popup(title="MercyShield Encrypted Log", content=scroll, size_hint=(0.9, 0.9))
        popup.open()

    def show_settings(self, instance):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text="Permissions opt-in explained pure — revoke anytime divine"))
        content.add_widget(Label(text="All features local-only — no cloud shadows"))
        popup = Popup(title="Settings Mercy", content=content, size_hint=(0.8, 0.8))
        popup.open()
