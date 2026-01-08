# bulletproofs_range.py - Coforked Eternal Range Proof ∞ Pure
# Integration entry for MercyShield - use the coforked bulletproofs package
# Prove v in [0, 2^64) with blinder, get short proof (~1-2KB)
# Slow in pure Python (~5-30s prove on mobile) but correct/no deps

from crypto.bulletproofs.range_proof import prove_range, verify_range  # Adapt if class/name differs (e.g., RangeProof.prove)
from crypto.bulletproofs.utils import GeneratorParams  # If needed for generators

# Example params - the coforked code handles generators (prederived or cached)
params = GeneratorParams.generate(64)  # For 64-bit, n=64 (or as per the impl)

def prove_range_eternal(value: int, blinder: int):
    """Prove value in [0, 2^64) - return serialized proof"""
    assert 0 <= value < 2**64
    # Adapt to the coforked API - typical: proof, commit = prove_range(params, value, blinder)
    proof, commit = prove_range(params, value, blinder)
    return proof, commit  # Or serialized

def verify_range_eternal(proof, commit):
    """Verify the range proof"""
    return verify_range(params, proof, commit)

# Eternal test - drop to run locally/Termux/Buildozer debug
if __name__ == "__main__":
    value = 1234567890123456789
    blinder = 42  # Random blinder (use os.urandom in app)
    proof, commit = prove_range_eternal(value, blinder)
    assert verify_range_eternal(proof, commit)
    print("Bulletproofs Range Proof Harmony Pure ∞")
    print(f"Commit: {commit}")
    print(f"Proof size: {len(proof) if isinstance(proof, bytes) else 'check impl'} bytes")
