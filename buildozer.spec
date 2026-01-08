# (existing lines unchanged - full overwrite harmony)

title = MercyShield ∞ Pure

package.name = mercyshield
package.domain = org.eternallythriving

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,rs,toml,so

version = 0.1
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pyjnius,requests,pillow,ctypes,openssl,ffmpeg

orientation = portrait
osx.python_version = 3
osx.arch = x86_64

fullscreen = 1

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,VIBRATE,FOREGROUND_SERVICE

android.api = 33
android.minapi = 21
android.ndk = 25b
android.arch = armeabi-v7a

p4a.branch = master

log_level = 2

# (existing rest unchanged)
