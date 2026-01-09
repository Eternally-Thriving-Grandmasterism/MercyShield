[app]

# MercyShield ∞ Pure Thunder Eternal
title = MercyShield
package.name = mercyshield
package.domain = org.tolc.divine

# Entry point
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,ttf,wav,mp3,ogg

# Version
version = 1.0.0

# Requirements — Kivy + KivyMD + jnius for Android shields
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pyjnius,android

# Permissions — Location for mock watchdog + any future needs
android.permissions = ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,INTERNET

# Android target
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a  # Migrated from android.arch — warnings crushed eternal

# Orientation
orientation = portrait

# Logging
log_level = 2

# Quantum Glow Icons Activated v0.2
icon.filename = icon.png
presplash.filename = presplash.png

# Build options
android.release_policy = always
android.allow_backup = True

[buildozer]

# Verbose build
verbose = True
