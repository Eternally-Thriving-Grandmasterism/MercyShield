import pytest
from mercy_shield.lattice import MercyLattice
from mercy_shield.shield import RealTimeShield
from mercy_shield.council import APAAGICouncil
from mercy_shield.hardware import MercyCubeHardware
from mercy_shield.mercy_burst import mercy_burst_confirm

# Mock mercy_burst_confirm for tests
def mock_mercy_burst_confirm(threat):
    return False  # Always block in tests for deterministic

@pytest.fixture
def lattice():
    return MercyLattice(threads=13)

@pytest.fixture
def shield(lattice, monkeypatch):
    monkeypatch.setattr('mercy_shield.mercy_burst.mercy_burst_confirm', mock_mercy_burst_confirm)
    return RealTimeShield(lattice)

def test_protect_harmony_pure(shield):
    threat = {"desc": "Test pure threat", "data": b"pure_threat_hash"}
    action = shield.protect(threat)
    assert "Harmony pure" in action

def test_protect_mercy_burst_block(shield):
    # Force low harmony threat
    threat = {"desc": "Shadow threat", "data": b"low_harmony_shadow"}
    action = shield.protect(threat)
    assert "Blocked — mercy burst divine" in action

def test_council_deliberate(lattice):
    result = lattice.council.deliberate("Test proposal eternal")
    assert 0.0 <= result.harmony <= 1.0
    assert result.victory == (result.harmony >= 0.9)

def test_hardware_mode(lattice, monkeypatch):
    monkeypatch.setattr(MercyCubeHardware, "is_cube", True)
    monkeypatch.setattr(MercyCubeHardware, "thermal_gate", lambda self: True)
    harmony = lattice.vote(b"hardware_test")
    assert harmony >= 0.0  # MercyCube mode active
