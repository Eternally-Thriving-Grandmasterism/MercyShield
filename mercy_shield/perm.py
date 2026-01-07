PERMISSIONS = [
    "android.permission.INTERNET",
    "android.permission.ACCESS_NETWORK_STATE",
    "android.permission.QUERY_ALL_PACKAGES",
    "android.permission.BIND_ACCESSIBILITY_SERVICE"
]

def request_permissions():
    print("MercyShield requests only essential permissions — one time, explained pure.")
    # In Kivy/Android: use pyjnius or buildozer to request
