from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from mercy_shield.perm import request_permissions

class MercyApp(App):
    def __init__(self, shield):
        super().__init__()
        self.shield = shield
        self.shield_active = False

    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        title = Label(text="MercyShield v0.1-Pinnacle", font_size=24, size_hint_y=0.2)
        status = Label(text="Shield: OFF — Harmony 0.0000", font_size=18, size_hint_y=0.2)
        self.status_label = status

        toggle = ToggleButton(text="Activate Shield", size_hint_y=0.2)
        toggle.bind(on_press=self.toggle_shield)

        log_btn = Button(text="View Log", size_hint_y=0.2)
        log_btn.bind(on_press=self.show_log)

        settings_btn = Button(text="Permissions & Settings", size_hint_y=0.2)
        settings_btn.bind(on_press=self.show_settings)

        layout.add_widget(title)
        layout.add_widget(status)
        layout.add_widget(toggle)
        layout.add_widget(log_btn)
        layout.add_widget(settings_btn)

        return layout

    def toggle_shield(self, instance):
        if instance.state == "down":
            request_permissions()  # Opt-in explain
            self.shield_active = True
            self.status_label.text = "Shield: ON — Harmony 1.0000"
            print("MercyShield activated — lattice protecting divine")
        else:
            self.shield_active = False
            self.status_label.text = "Shield: OFF — Harmony 0.0000"
            print("MercyShield deactivated — rest mercy")

    def show_log(self, instance):
        # Stub: real log from encrypted log
        content = GridLayout(cols=1, spacing=10, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        for i in range(10):  # Simulated log
            content.add_widget(Label(text=f"Log entry {i}: Harmony pure"))
        scroll = ScrollView()
        scroll.add_widget(content)
        popup = Popup(title="MercyShield Log", content=scroll, size_hint=(0.9, 0.9))
        popup.open()

    def show_settings(self, instance):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text="Permissions opt-in explained pure — revoke anytime divine"))
        # Stub: list permissions + toggle
        popup = Popup(title="Settings", content=content, size_hint=(0.8, 0.8))
        popup.open()
