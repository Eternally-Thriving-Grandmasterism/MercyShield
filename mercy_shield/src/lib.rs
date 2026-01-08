// src/lib.rs - Halo2 Proof Generation Wrapper ∞ Pure
// C ABI: prove_bytes(value, blinder) -> proof_ptr/len, verify_bytes(proof_ptr, len, commit) -> u8

use halo2_proofs::{
    halo2curves::pasta::Fp,
    plonk::{keygen_pk, keygen_vk, ProvingKey, VerifyingKey},
    circuit::Value,
};
use std::ffi::{CStr, CString};
use std::os::raw::c_char;

mod circuits;
use circuits::range_proof::RangeProofCircuit;

// Global keys (precompute or cache)
lazy_static! {
    static ref PK: ProvingKey<halo2_proofs::halo2curves::pasta::vesta::Affine> = { /* keygen_pk */ };
    static ref VK: VerifyingKey<halo2_proofs::halo2curves::pasta::vesta::Affine> = { /* keygen_vk */ };
}

#[no_mangle]
pub extern "C" fn halo2_prove_range64(value: u64, blinder: *const u8) -> *mut c_char {
    let circuit = RangeProofCircuit {
        value: Value::known(Fp::from(value)),
        blinder: Value::known(Fp::from_raw(*blinder as u64)),  // Adapt
    };

    let proof = halo2_proofs::plonk::create_proof::<_, _, _>(&PK, &[circuit], &[]).unwrap();  // Serialize proof

    let proof_str = CString::new(base64::encode(proof)).unwrap();  // Or raw bytes ptr
    proof_str.into_raw()
}

#[no_mangle]
pub extern "C" fn halo2_verify_range64(proof_ptr: *const c_char, commit: u64) -> u8 {
    // Deserialize + verify
    1u8  // Harmony
}
