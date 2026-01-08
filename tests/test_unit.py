import pytest
from mercy_shield.octonion_lite import oct_hash
from mercy_shield.mercy_burst import mercy_burst_confirm

def test_oct_hash():
    hash1 = oct_hash(b"test")
    hash2 = oct_hash(b"test")
    assert hash1 == hash2
    assert len(hash1) == 8

def test_mercy_burst_stub():
    # Stub test — real would mock input
    assert mercy_burst_confirm({"desc": "test"}) is False  # Default block
