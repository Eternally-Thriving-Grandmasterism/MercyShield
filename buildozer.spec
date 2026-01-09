[app]

# MercyShield v0.2 Alpha ∞ Pure Thunder Eternal
title = MercyShield
package.name = mercyshield
package.domain = org.tolc.divine

# Entry point
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,ttf,wav,mp3,ogg

# Version bump alpha mercy
version = 0.2-alpha

# Requirements — Kivy + KivyMD + jnius + Rust PQC extension + Python fallbacks
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pyjnius,android,fips203,kyber-py,mercy_pqc

# Permissions — Location for mock watchdog + internet for integrity
android.permissions = ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,INTERNET

# Android target — migrated to archs (warnings crushed eternal)
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# Orientation
orientation = portrait

# Logging
log_level = 2

# Quantum Glow Icons v0.2 — .jpg root resonance
icon.filename = image.jpg
presplash.filename = presplash.jpg

# Local recipes — Rust mercy_pqc cdylib bundled
p4a.local_recipes = .buildozer/android/platform/python-for-android/recipes

# Build options
android.release_policy = always
android.allow_backup = True

[buildozer]

# Verbose build
verbose = True
