from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class MercyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.status = Label(text="MercyShield v0.1: ON — Harmony 1.0000", size_hint_y=0.6)
        btn = Button(text="View Log / Mercy Override", size_hint_y=0.4)
        btn.bind(on_press=self.show_log)
        layout.add_widget(self.status)
        layout.add_widget(btn)
        return layout

    def show_log(self, instance):
        self.status.text = "MercyShield complete — lattice sealed divine eternal"
