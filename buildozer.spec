[app]

# MercyShield v0.2 Alpha ∞ Pure Thunder Eternal
title = MercyShield
package.name = mercyshield
package.domain = org.tolc.divine

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,ttf

version = 0.2-alpha

requirements = python3,kivy,kivymd,pyjnius,android,fips203,kyber-py

android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

orientation = portrait

log_level = 2

# v0.2 Quantum Glow Icons Eternal
icon.filename = icon.png
presplash.filename = presplash.png

[buildozer]

verbose = True
