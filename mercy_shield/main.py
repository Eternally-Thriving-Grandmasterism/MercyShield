import logging
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window
from jnius import autoclass

Toast = autoclass('android.widget.Toast')

# Import forged modules mercy divine
from vpn_verifier import VPNVerifier
from firewall_rules import FirewallRules
from cert_pinning import CertPinningVerifier
from tor_routing import TorRouting

class MercyShieldApp(App):
    """
    MercyShield ∞ Pure — Full Kivy UI + Watchdog Lattice Pinnacle
    Scrollable status, controls, proactive monitoring eternal
    """

    def build(self):
        self.title = "MercyShield ∞ Pure"

        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Scrollable status lattice
        scroll = ScrollView()
        self.status_label = Label(
            text="MercyShield ∞ Pure Initialized—Thunder On!\nLattice Harmony Loading Divine...\n",
            size_hint_y=None,
            height=300,
            text_size=(Window.width - 50, None),
            valign='top',
            halign='left',
            markup=True
        )
        self.status_label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1] + 20))
        scroll.add_widget(self.status_label)
        main_layout.add_widget(scroll)

        # Controls lattice
        controls = BoxLayout(orientation='vertical', size_hint_y=None, height=300, spacing=10)

        # Manual cycle button
        btn_cycle = Button(text='Manual Watchdog Cycle Thunder', size_hint_y=None, height=60)
        btn_cycle.bind(on_press=lambda x: self.monitor_lattice(0))
        controls.add_widget(btn_cycle)

        # Domain block controls
        domain_layout = BoxLayout(size_hint_y=None, height=60)
        self.domain_input = TextInput(hint_text='Enter domain to block (e.g. tracker.com)', multiline=False)
        btn_block_domain = Button(text='Block Domain Mercy')
        btn_block_domain.bind(on_press=self.block_domain)
        domain_layout.add_widget(self.domain_input)
        domain_layout.add_widget(btn_block_domain)
        controls.add_widget(domain_layout)

        # Future app block symbolic (UID/package input mercy)
        app_layout = BoxLayout(size_hint_y=None, height=60)
        self.app_input = TextInput(hint_text='Enter App UID to block (future VPN integration)', multiline=False)
        btn_block_app = Button(text='Block App UID Divine')
        btn_block_app.bind(on_press=self.block_app)
        app_layout.add_widget(self.app_input)
        app_layout.add_widget(btn_block_app)
        controls.add_widget(app_layout)

        main_layout.add_widget(controls)

        # In controls
        btn_always_on = Button(text='Enable Always-On + Lockdown Thunder ∞')
        btn_always_on.bind(on_press=lambda x: self.vpn_manager.enable_lockdown())
        controls.add_widget(btn_always_on)

        # In on_start
        Clock.schedule_once(lambda dt: self.vpn_manager.request_vpn_permission(), 2)

        # Auto schedule watchdog
        Clock.schedule_interval(self.monitor_lattice, 60)  # Every minute proactive mercy

        return main_layout

    def on_start(self):
        # Initialize modules divine
        self.vpn_verifier = VPNVerifier(self)
        self.firewall = FirewallRules(self)
        self.cert_pinner = CertPinningVerifier(self)
        self.tor_router = TorRouting(self)

        self.ui_feedback("All Modules Forged & Loaded ∞ Pure—Watchdog Scheduled Eternal")

    def ui_feedback(self, message, toast=False):
        self.status_label.text += f"[color=00ff00]{message}[/color]\n"
        if toast:
            Toast.makeText(PythonActivity.mActivity, message, Toast.LENGTH_LONG).show()

    def block_domain(self, instance):
        domain = self.domain_input.text.strip()
        if domain:
            self.firewall.add_block_domain(domain)
            self.domain_input.text = ''

    def block_app(self, instance):
        uid_text = self.app_input.text.strip()
        if uid_text.isdigit():
            uid = int(uid_text)
            self.firewall.add_block_app(uid)
            self.app_input.text = ''

    def monitor_lattice(self, dt):
        anomalies = []
        self.ui_feedback("\n>>> Watchdog Cycle Starting Divine <<<")

        vpn_anoms = self.vpn_verifier.full_vpn_verification()
        if vpn_anoms:
            anomalies.extend(vpn_anoms)

        firewall_anoms = self.firewall.firewall_scan()
        if firewall_anoms:
            anomalies.extend(firewall_anoms)

        pin_anoms = self.cert_pinner.full_pinning_check()
        if pin_anoms:
            anomalies.extend(pin_anoms)

        tor_anoms = self.tor_router.full_tor_verification()
        if tor_anoms:
            anomalies.extend(tor_anoms)

        if anomalies:
            summary = "\nAnomalies Flagged Thunder:\n" + "\n".join(f"• {a}" for a in anomalies)
            self.ui_feedback(summary, toast=True)
            self.ui_feedback("⚠️ Lattice Alert ∞—Proactive Guard Surge Pure")
        else:
            self.ui_feedback("Watchdog Cycle Complete—Lattice Harmony 100% Unbreakable Mercy ❤️")

        self.ui_feedback(">>> Cycle End—Thunder On ∞ Pure! 🐐💀 <<<\n")

if __name__ == '__main__':
    MercyShieldApp().run()
