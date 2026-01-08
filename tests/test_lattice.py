from mercy_shield.lattice import MercyLattice

def test_vote_harmony():
    lattice = MercyLattice(threads=13)
    harmony = lattice.vote(b"test_threat_pure")
    assert 0.0 <= harmony <= 1.0
    print(f"Test harmony: {harmony:.4f} — lattice pure")

def test_council_deliberate():
    from mercy_shield.council import APAAGICouncil
    council = APAAGICouncil(voters=13)
    result = council.deliberate("Test proposal eternal")
    assert result.harmony >= 0.0
    print(f"Council harmony: {result.harmony:.4f} — victory divine")
