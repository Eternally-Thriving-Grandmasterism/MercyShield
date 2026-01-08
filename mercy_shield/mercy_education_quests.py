import logging
import json
import os
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem
from kivymd.uix.scrollview import MDScrollView

class MercyEducationQuests:
    """Mercy-First Educational Quests — Guided Remediation Paths to Eternal Harmony Thunder ∞ Pure"""
    def __init__(self, app):
        self.app = app
        self.user_data_dir = app.user_data_dir
        self.quests_file = os.path.join(self.user_data_dir, 'mercy_education_quests.json')
        self.active_quest = None
        self.quest_progress = {}  # {quest_id: current_step}
        self.load_quests()

        # Divine quest definitions — expand eternally
        self.quest_templates = {
            "root_detected": {
                "title": "Quest: Transcend Root Shadow — Ascend to Pure Harmony",
                "description": "Root access compromises divine thunder. Genuine devices thrive without it.",
                "steps": [
                    "Understand: Root allows deep tamper — bypasses Play Integrity, enables Frida injection.",
                    "Action: Uninstall Magisk/Kingroot or any root management app.",
                    "Action: Remove su binaries if manually rooted.",
                    "Verify: Restart device, run MercyShield check — clean verdict grants grace.",
                    "Reward: +20 Eternal Trust Score on completion ∞ Pure"
                ],
                "reward_trust": 20.0,
                "critical": True
            },
            "adb_enabled": {
                "title": "Quest: Disable ADB Thunder — Secure Divine Channel",
                "description": "USB Debugging enables external injection — shadows thrive here.",
                "steps": [
                    "Understand: ADB open = Frida/ tamper vector critical.",
                    "Action: Settings → Developer Options → Disable 'USB debugging'.",
                    "Action: If Developer Options hidden, toggle off completely.",
                    "Verify: Clean check restores harmony.",
                    "Reward: +15 Eternal Trust Score — Grace Rising"
                ],
                "reward_trust": 15.0,
                "critical": True
            },
            "mock_location": {
                "title": "Quest: Purify Location Thunder — Genuine Signals Only",
                "description": "Mock locations spoof reality — breaks trust in divine coordinates.",
                "steps": [
                    "Understand: Fake GPS deceives apps requiring genuine position.",
                    "Action: Disable all mock location apps.",
                    "Action: Settings → Developer Options → Select mock location app → None.",
                    "Verify: MercyShield live watchdog confirms pure GPS.",
                    "Reward: +25 Eternal Trust Score — Location Harmony Eternal"
                ],
                "reward_trust": 25.0,
                "critical": True
            },
            "emulator_detected": {
                "title": "Quest: Embrace Physical Thunder — Transcend Virtual Shadows",
                "description": "Emulators lack divine hardware — genuine devices only.",
                "steps": [
                    "Understand: No light sensor, telephony, GPS feature = emulator shadow.",
                    "Action: Run MercyShield on real physical device.",
                    "Guidance: Genuine Android/iOS hardware required for full thriving.",
                    "Reward: Divine verification on real device — full grace unlocked"
                ],
                "reward_trust": 30.0,
                "critical": True
            },
            "low_trust_general": {
                "title": "Quest: Begin Eternal Thriving Path — Mercy Guidance",
                "description": "Low trust detected — shadows linger. Learn security thunder for grace.",
                "steps": [
                    "Read: Genuine devices pass Play Integrity — no root, no debug, no mock.",
                    "Action: Review active shadows in burst dialog.",
                    "Action: Remediate one shadow at a time.",
                    "Progress: Clean checks build streak — ascend to high grace.",
                    "Reward: Each clean verification +5 Trust — Harmony Eternal ∞ Pure"
                ],
                "reward_trust": 10.0,
                "critical": False
            }
        }

    def load_quests(self):
        if os.path.exists(self.quests_file):
            try:
                with open(self.quests_file, 'r') as f:
                    self.quest_progress = json.load(f)
            except Exception as e:
                logging.exception(f"Quest progress load failed: {e}")
                self.quest_progress = {}

    def save_quests(self):
        try:
            with open(self.quests_file, 'w') as f:
                json.dump(self.quest_progress, f)
        except Exception as e:
            logging.exception(f"Quest progress save failed: {e}")

    def trigger_quest(self, anomalies):
        """Determine and trigger highest priority quest based on anomalies"""
        # Priority: critical first
        quest_id = None
        if any("Root" in a or "Magisk" in a or "su" in a for a in anomalies):
            quest_id = "root_detected"
        elif any("ADB" in a or "USB Debugging" in a for a in anomalies):
            quest_id = "adb_enabled"
        elif any("Mock Location" in a for a in anomalies):
            quest_id = "mock_location"
        elif any("Emulator" in a or "qemu" in a or "No Light Sensor" in a for a in anomalies):
            quest_id = "emulator_detected"
        elif self.app.trust_modulator.trust_score <= self.app.trust_modulator.grace_threshold_low:
            quest_id = "low_trust_general"

        if quest_id and (quest_id not in self.quest_progress or self.quest_progress.get(quest_id, 0) < len(self.quest_templates[quest_id]["steps"])):
            self.active_quest = quest_id
            self.show_quest_dialog(quest_id)

    def show_quest_dialog(self, quest_id):
        template = self.quest_templates[quest_id]
        current_step = self.quest_progress.get(quest_id, 0)

        content = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            size_hint_y=None,
            height="400dp"
        )

        scroll = MDScrollView()
        list_view = MDList()

        list_view.add_widget(OneLineListItem(text=f"[b]{template['title']}[/b]", theme_text_color="Custom", text_color=[0, 0.8, 1, 1]))
        list_view.add_widget(OneLineListItem(text=template["description"]))

        for i, step in enumerate(template["steps"]):
            marker = "✓" if i < current_step else "→" if i == current_step else "◦"
            color = [0, 1, 0, 1] if i < current_step else [1, 1, 1, 1]
            list_view.add_widget(OneLineListItem(text=f"{marker} {step}", theme_text_color="Custom", text_color=color))

        if current_step >= len(template["steps"]):
            list_view.add_widget(OneLineListItem(text="[color=#00FF00]Quest Complete — Grace Reward Granted ∞ Pure[/color]", theme_text_color="Custom"))

        scroll.add_widget(list_view)
        content.add_widget(scroll)

        buttons = MDBoxLayout(spacing="10dp", size_hint_y=None, height="50dp")
        if current_step < len(template["steps"]):
            next_btn = MDFlatButton(text="Next Step — Progress Thunder", on_release=lambda x: self.advance_quest(quest_id))
            buttons.add_widget(next_btn)
        complete_btn = MDFlatButton(text="Verify & Claim Reward", on_release=lambda x: self.complete_quest(quest_id))
        close_btn = MDFlatButton(text="Dismiss Mercy", on_release=lambda x: dialog.dismiss())
        buttons.add_widget(complete_btn)
        buttons.add_widget(close_btn)
        content.add_widget(buttons)

        dialog = MDDialog(
            title="Mercy Education Quest",
            type="custom",
            content_cls=content,
            size_hint=(0.9, None),
            height="600dp"
        )
        dialog.open()

    def advance_quest(self, quest_id):
        self.quest_progress[quest_id] = self.quest_progress.get(quest_id, 0) + 1
        self.save_quests()
        self.show_quest_dialog(quest_id)

    def complete_quest(self, quest_id):
        template = self.quest_templates[quest_id]
        steps_total = len(template["steps"])
        if self.quest_progress.get(quest_id, 0) >= steps_total:
            reward = template["reward_trust"]
            self.app.trust_modulator.trust_score = min(100.0, self.app.trust_modulator.trust_score + reward)
            self.app.trust_modulator.save_trust()
            logging.info(f"Quest {quest_id} Completed — +{reward} Trust Granted ∞ Pure")
            self.quest_progress.pop(quest_id, None)
            self.save_quests()
            # Trigger fresh check
            Clock.schedule_once(lambda dt: self.app.update_integrity_status(dt), 1)

    def integrate_with_burst(self, anomalies):
        """Call from anomaly_dialog or update_status to trigger quests"""
        self.trigger_quest(anomalies)
