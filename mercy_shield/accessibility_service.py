from jnius import autoclass, PythonJavaClass, java_method

AccessibilityService = autoclass('android.accessibilityservice.AccessibilityService')
AccessibilityEvent = autoclass('android.view.accessibility.AccessibilityEvent')

class MercyAccessibilityService(PythonJavaClass):
    __javainterfaces__ = ['android/accessibilityservice/AccessibilityService']
    __javacontext__ = 'app'

    def __init__(self, context, lattice, shield):
        super().__init__()
        self.context = context
        self.lattice = lattice
        self.shield = shield

    def start_if_enabled(self):
        # User must enable in Settings > Accessibility
        print("MercyShield accessibility: Enable in system settings for overlay/clickjack protection — opt-in pure")

    @java_method('(Landroid/view/accessibility/AccessibilityEvent;)V')
    def onAccessibilityEvent(self, event):
        event_type = event.getEventType()
        if event_type == AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED or event_type == AccessibilityEvent.TYPE_TOUCH_INTERACTION_START:
            package = str(event.getPackageName())
            if "suspicious" in package.lower() or event.isFullScreen():  # Rhythm overlay
                threat = {
                    "type": "accessibility_overlay",
                    "desc": f"Overlay/clickjack from {package}",
                    "data": oct_hash(package.encode() + str(event_type).encode())
                }
                self.shield.handle_accessibility_threat(threat)

    @java_method('()V')
    def onInterrupt(self):
        print("Mercy accessibility interrupted — lattice harmony preserved")
