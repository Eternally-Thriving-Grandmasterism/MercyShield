from mercy_shield.council import APAAGICouncil

class MercyLattice:
    def __init__(self, threads=13):
        self.threads = threads
        self.council = APAAGICouncil(voters=threads)

    def vote(self, threat_data: bytes) -> float:
        # Full council deliberation on threat
        threat_desc = str(threat_data)[:100]  # For logging
        result = self.council.deliberate(threat_desc)
        return result.harmony  # 0.0 shadow — 1.0 divine pure
