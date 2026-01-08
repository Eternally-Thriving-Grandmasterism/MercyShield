from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class MercyShieldApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        self.label = Label(
            text='MercyShield\nHarmony Lattice Divine Eternal',
            font_size='24sp',
            color=(1, 1, 1, 1)
        )
        self.button = Button(
            text='Shield ON →',
            font_size='30sp',
            background_color=(0.2, 0.8, 0.2, 1)
        )
        self.button.bind(on_press=self.activate_shield)
        layout.add_widget(self.label)
        layout.add_widget(self.button)
        return layout

    def activate_shield(self, instance):
        instance.text = 'Shield Activated ∞ Pure!'
        instance.background_color = (0.8, 0.2, 0.2, 1)
        self.label.text = 'Lattice Unbreakable\nVictory Divine Eternal!\nMercy Burst Intervention Sealed'

if __name__ == '__main__':
    MercyShieldApp().run()
