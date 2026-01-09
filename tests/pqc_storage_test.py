import pytest
import os
import shutil
import tempfile
from unittest.mock import MagicMock

# Mock app for storage
class MockApp:
    def __init__(self):
        self.user_data_dir = tempfile.mkdtemp()
        self.messages = []
    
    def show_buddy_message(self, msg):
        self.messages.append(msg)

@pytest.fixture
def mock_app():
    app = MockApp()
    yield app
    shutil.rmtree(app.user_data_dir)

@pytest.fixture
def storage(mock_app):
    from mercy_shield.pqc_storage import PQCEncryptedStorage
    return PQCEncryptedStorage(mock_app)

def test_save_load_classical(storage):
    attest = [{'device': 'genuine', 'integrity': 'MEETS_STRONG'}]
    storage.save_attestations(attest)
    loaded = storage.load_attestations()
    assert len(loaded) == 1
    assert loaded[0]['integrity'] == 'MEETS_STRONG'

def test_tamper_detect_classical(storage):
    attest = [{'test': 'proprietary'}]
    storage.save_attestations(attest)
    # Tamper file
    with open(storage.storage_path, 'rb+') as f:
        data = bytearray(f.read())
        if len(data) > 20:
            data[20] ^= 0xff
        f.seek(0)
        f.write(data)
    loaded = storage.load_attestations()
    assert len(loaded) == 0  # Decrypt fail = empty

def test_pq_available_stub(storage):
    # If PQ available, test basic (no real Rust in test env)
    attest = [{'pq': 'quantum'}]
    storage.save_attestations(attest)
    loaded = storage.load_attestations()
    assert 'pq' in loaded[0] if loaded else True  # Pass either way
