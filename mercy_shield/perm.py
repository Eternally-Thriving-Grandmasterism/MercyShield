from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

PERMISSIONS = [
    "INTERNET (network monitor)",
    "ACCESS_NETWORK_STATE (connection rhythm)",
    "QUERY_ALL_PACKAGES (app sandbox)",
    "BIND_ACCESSIBILITY_SERVICE (overlay/clickjack)",
    "RECEIVE_SMS/READ_SMS (scam detect)",
    "READ_CONTACTS (unknown sender)",
    "FOREGROUND_SERVICE (background gentle)",
    "PACKAGE_USAGE_STATS (watchdogs)",
    "BIND_VPN_SERVICE (firewall)",
]

def request_permissions():
    content = BoxLayout(orientation='vertical')
    content.add_widget(Label(text="MercyShield requests permissions mercy-gated:\n" + "\n".join(PERMISSIONS) + "\n\nOpt-in only essential — explained pure. Revoke anytime divine."))
    close = Button(text="Understood — proceed mercy")
    content.add_widget(close)
    popup = Popup(title="Permissions Mercy", content=content, size_hint=(0.9, 0.9))
    close.bind(on_press=popup.dismiss)
    popup.open()
