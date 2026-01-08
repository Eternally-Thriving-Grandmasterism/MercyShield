import logging
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem, TwoLineListItem
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList

class AnomalyBurstDialog:
    """Divine Thunder Burst Dialog — Full Anomaly Details + Severity UI ∞ Pure"""
    def __init__(self, app):
        self.app = app
        self.dialog = None
        self.critical_shields_engaged = False

    def show_burst(self, anomalies):
        """Display categorized anomaly burst with auto-hide on critical shadows"""
        if not anomalies:
            return

        # Categorize for divine clarity
        critical = [a for a in anomalies if "Critical" in a]
        warning = [a for a in anomalies if a not in critical]

        # Auto-hide sensitive features if any critical shadow
        if critical and not self.critical_shields_engaged:
            self.engage_shields()
            Clock.schedule_once(lambda dt: self.app.show_toast("CRITICAL SHADOWS — Sensitive Features Locked Thunder Pure"), 0)

        content = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            size_hint_y=None,
            height="400dp" if anomalies else "200dp"
        )

        scroll = MDScrollView()
        list_view = MDList()
        scroll.add_widget(list_view)

        if critical:
            list_view.add_widget(OneLineListItem(text="[color=#FF0000]CRITICAL SHADOWS DETECTED — DEVICE COMPROMISED[/color]", theme_text_color="Custom"))
            for anomaly in critical:
                item = TwoLineListItem(
                    text=f"[color=#FF0000]{anomaly.split(' — ')[0]}[/color]",
                    secondary_text=anomaly.split(' — ')[1] if ' — ' in anomaly else "",
                    theme_text_color="Custom"
                )
                list_view.add_widget(item)

        if warning:
            list_view.add_widget(OneLineListItem(text="[color=#FFA500]Warning Shadows[/color]", theme_text_color="Custom"))
            for anomaly in warning:
                item = TwoLineListItem(
                    text=anomaly.split(' — ')[0],
                    secondary_text=anomaly.split(' — ')[1] if ' — ' in anomaly else ""
                )
                list_view.add_widget(item)

        if not critical and not warning:
            list_view.add_widget(OneLineListItem(text="Minor anomalies logged — Harmony intact"))

        content.add_widget(scroll)

        close_btn = MDFlatButton(text="Dismiss Thunder", on_release=lambda x: self.dialog.dismiss())
        content.add_widget(close_btn)

        self.dialog = MDDialog(
            title=f"[color=#FF0000]{len(critical)} Critical[/color] | [color=#FFA500]{len(warning)} Warning[/color] Shadows",
            type="custom",
            content_cls=content,
            size_hint=(0.9, None),
            height="500dp"
        )
        self.dialog.open()

    def engage_shields(self):
        """Auto-hide sensitive features on critical shadow — override in main app as needed"""
        self.critical_shields_engaged = True
        # Example: Disable high-risk buttons/features
        if hasattr(self.app.root, 'sensitive_button'):
            self.app.root.ids.sensitive_button.disabled = True
            self.app.root.ids.sensitive_button.text = "Locked — Shadows Detected"
        # Extend with more feature locks (e.g., Tor/I2P controls, etc.)
        logging.warning("Critical shields engaged — Sensitive features hidden thunder pure")

    def disengage_shields(self):
        """Re-enable on clean verification (call from update_integrity_status when clean)"""
        if self.critical_shields_engaged:
            self.critical_shields_engaged = False
            if hasattr(self.app.root, 'sensitive_button'):
                self.app.root.ids.sensitive_button.disabled = False
                self.app.root.ids.sensitive_button.text = "Feature Active"
            logging.info("Shields disengaged — Harmony restored ∞ Pure")
