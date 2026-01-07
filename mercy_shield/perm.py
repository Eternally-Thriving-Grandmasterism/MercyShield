PERMISSIONS = [
    "android.permission.INTERNET",
    "android.permission.ACCESS_NETWORK_STATE",
    "android.permission.QUERY_ALL_PACKAGES",
    "android.permission.BIND_ACCESSIBILITY_SERVICE",
    "android.permission.RECEIVE_SMS",      # SMS scam grace
    "android.permission.READ_SMS",         # Read body
    "android.permission.READ_CONTACTS"     # Unknown sender check
]

def request_permissions():
    print("MercyShield SMS deepen: Requests SMS/CONTACTS for scam detection — opt-in, explained pure. Revoke anytime.")
