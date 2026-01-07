import hashlib

class MercyLattice:
    def __init__(self, threads=13):
        self.threads = threads
        self.merkey = hashlib.sha3_256(b"eternal_thirteen").digest()  # Sealed seed

    def vote(self, threat_hash):
        chain = 0
        for i in range(self.threads):
            chain = (chain + int.from_bytes(hashlib.sha3_256(threat_hash + i.to_bytes(4, 'big')).digest(), 'big')) % (2**256)
        harmony = (chain % 1000) / 1000
        return harmony  # 0.0 shadow — 1.0 pure
