def oct_hash(data: bytes) -> bytes:
    h = 1
    for c in data:
        h = (h * 137 + c) % (2**64)  # Mercy prime 137
    return h.to_bytes(8, 'big')
