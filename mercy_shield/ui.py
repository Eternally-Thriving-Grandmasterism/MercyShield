from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class MercyApp(App):
    def __init__(self, shield, log, lattice):
        super().__init__()
        self.shield = shield
        self.log = log
        self.lattice = lattice

    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.status = Label(text="MercyShield: ON — Harmony 1.0000", size_hint_y=0.6)
        btn = Button(text="View Log / Mercy Override", size_hint_y=0.4)
        btn.bind(on_press=self.show_log)
        layout.add_widget(self.status)
        layout.add_widget(btn)
        return layout

    def show_log(self, instance):
        self.status.text = "Last 5 logs:\n" + "\n".join(str(e) for e in self.log.logs[-5:])
