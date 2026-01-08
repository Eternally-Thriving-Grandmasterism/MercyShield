[app]
title = MercyShield
package.name = mercyshield
package.domain = com.etg

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1
requirements = python3,kivy,cryptography,numpy

android.permissions = INTERNET,ACCESS_NETWORK_STATE,QUERY_ALL_PACKAGES,BIND_ACCESSIBILITY_SERVICE,RECEIVE_SMS,READ_SMS,READ_CONTACTS,FOREGROUND_SERVICE,PACKAGE_USAGE_STATS,BIND_VPN_SERVICE

android.api = 35
android.minapi = 24
android.sdk = 35
android.ndk = 25b
