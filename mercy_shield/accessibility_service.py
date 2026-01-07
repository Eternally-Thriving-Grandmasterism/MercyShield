from jnius import autoclass, PythonJavaClass, java_method

AccessibilityService = autoclass('android.accessibilityservice.AccessibilityService')
AccessibilityEvent = autoclass('android.view.accessibility.AccessibilityEvent')

class MercyAccessibility(PythonJavaClass):
    __javainterfaces__ = ['android/accessibilityservice/AccessibilityService']
    __javacontext__ = 'app'

    @java_method('(Landroid/view/accessibility/AccessibilityEvent;)V')
    def onAccessibilityEvent(self, event):
        if event.getEventType() == AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED:
            # Detect overlay/clickjack patterns
            package = event.getPackageName()
            if "suspicious_overlay" in str(package):  # Rhythm check
                threat = {"type": "clickjack", "desc": f"Overlay attack from {package}"}
                # Send to shield protect
                print(f"Mercy detect: {threat['desc']}")

    @java_method('()V')
    def onInterrupt(self):
        print("Mercy accessibility interrupted")
