// src/lib.rs - Halo2 Lightning Prove ∞ Pure Coforked
// Prove range hiding, return proof bytes ptr/len (ctypes read)

use halo2_proofs::{
    plonk::{create_proof, keygen_pk, keygen_vk},
    poly::kzg::{
        commitment::{KZGCommitmentScheme, ParamsKZG},
        multiopen::ProverSHPLONK,
    },
    transcript::{Blake2bWrite, Challenge255},
};
use halo2_proofs::halo2curves::bn256::{Bn256, G1Affine};
use lazy_static::lazy_static;
use rand::rngs::OsRng;
use std::sync::Arc;

mod circuits;
use circuits::range_proof::RangeProofCircuit;

lazy_static! {
    static ref PARAMS: ParamsKZG<Bn256> = ParamsKZG::<Bn256>::new(9);
    static ref PK: Arc<ProvingKey<G1Affine>> = Arc::new(keygen_pk(&*PARAMS, &RangeProofCircuit::default()).unwrap());
}

#[no_mangle]
pub extern "C" fn halo2_prove_range64(value: u64, blinder: u64, out_len: *mut usize) -> *mut u8 {
    let circuit = RangeProofCircuit {
        value: Value::known(Fp::from(value)),
        blinder: Value::known(Fp::from(blinder)),
    };

    let mut transcript = Blake2bWrite::<_, G1Affine, Challenge255<_>>::init(vec![]);

    create_proof::<KZGCommitmentScheme<Bn256>, ProverSHPLONK<'_, Bn256>, _, _, _, _>(
        &PARAMS, &PK, &[circuit], &[&[]], OsRng, &mut transcript,
    ).unwrap();

    let proof_bytes = transcript.finalize();

    unsafe { *out_len = proof_bytes.len(); }

    Box::into_raw(proof_bytes.into_boxed_slice()) as *mut u8
}

#[no_mangle]
pub extern "C" fn halo2_free_proof(ptr: *mut u8) {
    if !ptr.is_null() {
        unsafe { Box::from_raw(ptr); }
    }
}
