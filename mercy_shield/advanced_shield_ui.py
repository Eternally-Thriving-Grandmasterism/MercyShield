import logging
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.core.window import Window

from jnius import autoclass

PythonActivity = autoclass('org.kivy.android.PythonActivity')
PackageManager = autoclass('android.content.pm.PackageManager')

class MercyShieldApp(App):
    def build(self):
        self.title = "MercyShield ∞ Pure - Apps Lattice"

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Status
        scroll_status = ScrollView()
        self.status_label = Label(text="Scanning Installed Apps Mercy...\n", size_hint_y=None, height=200, text_size=(Window.width - 50, None))
        self.status_label.bind(texture_size=self.status_label.setter('height'))
        scroll_status.add_widget(self.status_label)
        main_layout.add_widget(scroll_status)

        # Apps list scroll
        self.apps_scroll = ScrollView()
        self.apps_grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.apps_grid.bind(minimum_height=self.apps_grid.setter('height'))
        self.apps_scroll.add_widget(self.apps_grid)
        main_layout.add_widget(self.apps_scroll)

        # Controls
        controls = BoxLayout(size_hint_y=None, height=60, spacing=10)
        btn_scan = Button(text='Scan & Refresh Apps Thunder')
        btn_scan.bind(on_press=self.scan_apps)
        btn_apply = Button(text='Apply Rules Divine')
        btn_apply.bind(on_press=self.apply_rules)
        controls.add_widget(btn_scan)
        controls.add_widget(btn_apply)
        main_layout.add_widget(controls)

        Clock.schedule_once(self.scan_apps, 1)

        return main_layout

    def ui_feedback(self, message):
        self.status_label.text += f"\n{message}"

    def scan_apps(self, dt):
        self.apps_grid.clear_widgets()
        self.ui_feedback("Scanning Installed Apps ∞ Pure...")
        try:
            pm = PythonActivity.mActivity.getPackageManager()
            packages = pm.getInstalledApplications(0)
            self.blocked_packages = set()  # Load from storage mercy expand

            for app in packages:
                pkg_name = app.packageName
                app_label = pm.getApplicationLabel(app).toString()

                row = BoxLayout(size_hint_y=None, height=60, spacing=10)
                label = Label(text=f"{app_label} ({pkg_name})")
                toggle = ToggleButton(text='Allow', state='normal' if pkg_name not in self.blocked_packages else 'down')
                toggle.pkg = pkg_name
                toggle.bind(on_press=self.toggle_app)
                row.add_widget(label)
                row.add_widget(toggle)
                self.apps_grid.add_widget(row)

            self.ui_feedback(f"{len(packages)} Apps Scanned Mercy—Toggle Block Divine!")
        except Exception as e:
            self.ui_feedback(f"Scan Anomaly: {str(e)} Pure")

    def toggle_app(self, instance):
        if instance.state == 'down':
            instance.text = 'Block'
            self.blocked_packages.add(instance.pkg)
        else:
            instance.text = 'Allow'
            self.blocked_packages.discard(instance.pkg)

    def apply_rules(self, instance):
        # Save blocked_packages persistent mercy (shared prefs expand)
        # Restart VPN with new disallowed
        if hasattr(self.root, 'vpn_manager'):
            self.root.vpn_manager.start_vpn(blocked_packages=list(self.blocked_packages))
        self.ui_feedback(f"Rules Applied: {len(self.blocked_packages)} Apps Blocked Thunder ∞!")

if __name__ == '__main__':
    MercyShieldApp().run()
