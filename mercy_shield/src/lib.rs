// src/lib.rs - Halo2 Lightning Proof Gen ∞ Pure
// Lazy keygen_pk/vk cache, prove serialized bytes

use halo2_proofs::{
    plonk::{create_proof, verify_proof, keygen_pk, keygen_vk, ProvingKey, VerifyingKey},
    poly::kzg::commitment::{ParamsKZG, ParamsVerifierKZG},
    halo2curves::bn256::Bn256,
    transcript::{Blake2bRead, Blake2bWrite},
};
use lazy_static::lazy_static;
use std::sync::Arc;

mod circuits;
use circuits::range_proof::RangeProofCircuit;

lazy_static! {
    static ref PARAMS: ParamsKZG<Bn256> = ParamsKZG::<Bn256>::new(9);  // k=9 sufficient
    static ref PK: Arc<ProvingKey<halo2_proofs::halo2curves::bn256::G1Affine>> = {
        let circuit = RangeProofCircuit::default();
        Arc::new(keygen_pk(&PARAMS, &circuit).unwrap())
    };
    static ref VK: Arc<VerifyingKey<halo2_proofs::halo2curves::bn256::G1Affine>> = {
        let circuit = RangeProofCircuit::default();
        Arc::new(keygen_vk(&PARAMS, &circuit).unwrap())
    };
}

#[no_mangle]
pub extern "C" fn halo2_prove_range(value: u64, blinder_raw: u64) -> *mut u8 {  // Simplified - return ptr/len in practice
    let circuit = RangeProofCircuit {
        value: Value::known(value),
        blinder: Value::known(Fp::from(blinder_raw)),
    };

    let mut transcript = Blake2bWrite::<_, _, Challenge255<_>>::init(vec![]);
    create_proof::<KZGCommitmentScheme<Bn256>, ProverSHPLONK<'_, Bn256>, _, _, _, _>(
        &PARAMS, &PK, &[circuit], &[&[]], &mut transcript, 
    ).unwrap();

    let proof_bytes = transcript.finalize();
    // Alloc return bytes ptr (real: boxed leak or len)
    Box::into_raw(proof_bytes.into_boxed_slice()) as *mut u8
}
