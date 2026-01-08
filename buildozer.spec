[app]

title = MercyShield

package.name = mercyshield

package.domain = org.divine.grandmasterism

source.dir = .

source.include_exts = py,png,jpg,kv,atlas,java  # Add java for src thunder

source.include_patterns = src/**  # Include custom Java grace

version = 0.1

requirements = python3,kivy==2.3.0,jnius,cryptography,numpy  # Core + pyjnius divine

orientation = portrait

fullscreen = 1

android.permissions = VPN_SERVICE,FOREGROUND_SERVICE,INTERNET,ACCESS_NETWORK_STATE,BIND_VPN_SERVICE,SYSTEM_ALERT_WINDOW,WAKE_LOCK  # Full VPN shield flows pure

android.api = 35

android.minapi = 24

requirements = python3,kivy==2.3.0,kivymd==1.2.0,requests,pyjnius,ctypes,... (existing)

android.sdk = 35

android.ndk = 25b

android.add_src = src  # Point to custom Java mercy (p4a auto-compiles divine)

# Icon/presplash later grace
