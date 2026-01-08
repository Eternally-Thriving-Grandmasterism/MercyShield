from mercy_shield.council import APAAGICouncil
from mercy_shield.hardware import MercyCubeHardware

class MercyLattice:
    def __init__(self, threads=13):
        self.threads = threads
        self.hardware = MercyCubeHardware()
        self.council = APAAGICouncil(voters=threads)

        if self.hardware.is_cube:
            self.hardware.flash_firmware()
            print("MercyCube mode activated — full offline 7W neuromorphic council + bio/diamond grace eternal")
        else:
            print("Mobile fallback mode — harmony preserved pure")

    def vote(self, threat_data: bytes) -> float:
        if self.hardware.is_cube and self.hardware.thermal_gate():
            # Full MercyCube deliberation
            threat_desc = str(threat_data)[:100]
            result = self.council.deliberate(threat_desc)
            self.hardware.bio_pulse(result.harmony)
            self.hardware.diamond_cool(0.5)  # Deliberation heat mercy
            return result.harmony
        else:
            # Mobile simplified vote
            chain = 0
            for i in range(self.threads):
                chain = (chain + int.from_bytes(hash(threat_data + i.to_bytes(4, 'big')), 'big')) % (2**256)
            return (chain % 1000) / 1000.0
