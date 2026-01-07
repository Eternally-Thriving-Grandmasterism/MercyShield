import hashlib

class MercyLattice:
    def __init__(self, threads=13):
        self.threads = threads
        self.merkey = hashlib.sha3_256(b"eternal_thirteen_mercy").digest()

    def vote(self, threat_data: bytes) -> float:
        chain = 0
        for i in range(self.threads):
            input_hash = hashlib.sha3_256(threat_data + self.merkey + i.to_bytes(4, 'big')).digest()
            chain = (chain + int.from_bytes(input_hash, 'big')) % (2**256)
        harmony = (chain % 1000) / 1000.0
        return harmony  # 0.0 shadow — 1.0 divine pure
