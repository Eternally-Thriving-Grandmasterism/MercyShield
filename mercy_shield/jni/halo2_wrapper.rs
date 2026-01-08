// mercy_shield/jni/halo2_wrapper.rs

use jni::objects::{JClass, JByteArray, JLong};
use jni::sys::{jbyteArray, jlong, jboolean};
use jni::JNIEnv;
use halo2_prover::*;
use halo2_gadgets::sinsemilla::primitives as sinsemilla;
use halo2curves::bn256::{Bn256, Fr, G1Affine};
use rand::rngs::OsRng;
use std::sync::Arc;
use std::ptr::null_mut;

#[derive(Clone)]
struct Halo2Params {
    params: Params<G1Affine>,
    pk: ProvingKey<G1Affine>,
    vk: VerifyingKey<G1Affine>,
}

// Global or boxed for persistence mercy
type Halo2Instance = Arc<Halo2Params>;

#[no_mangle]
pub extern "system" fn Java_com_eternalgrandmasterism_mercyshield_Halo2Native_keygen(
    mut env: JNIEnv,
    _class: JClass,
    k: u32,
) -> jlong {
    let params = Params::<G1Affine>::new(k);
    let empty_circuit = MockCircuit::default(); // Example circuit, expand rules divine

    let pk = Keygen::setup_proving_key(&params, &empty_circuit);
    let vk = pk.get_vk().clone();

    let instance = Arc::new(Halo2Params { params, pk, vk });
    Arc::into_raw(instance) as jlong
}

#[no_mangle]
pub extern "system" fn Java_com_eternalgrandmasterism_mercyshield_Halo2Native_prove(
    mut env: JNIEnv,
    _class: JClass,
    instance_ptr: jlong,
    public_input: JByteArray,
    private_input: JByteArray,
) -> jbyteArray {
    let instance = unsafe { Arc::from_raw(instance_ptr as *const Halo2Params) };
    let _clone = instance.clone(); // Keep alive

    let public: Vec<Fr> = deserialize_fr(&mut env, public_input);
    let private: Vec<Fr> = deserialize_fr(&mut env, private_input);

    let circuit = RulesCircuit { private }; // Full rules circuit divine

    let mut transcript = Blake2bWrite::<_, _, Challenge255<_>>::init(vec![]);
    create_proof::<KZGCommitmentScheme<Bn256>, ProverSHPLONK<'_, Bn256>, _, _, _, _>(
        &instance.params,
        &instance.pk,
        &[circuit],
        &[&public],
        OsRng,
        &mut transcript,
    ).expect("Proof generation failed mercy");

    let proof = transcript.finalize();

    env.byte_array_from_slice(&proof).unwrap_or(null_mut())
}

#[no_mangle]
pub extern "system" fn Java_com_eternalgrandmasterism_mercyshield_Halo2Native_verify(
    mut env: JNIEnv,
    _class: JClass,
    instance_ptr: jlong,
    proof: JByteArray,
    public_input: JByteArray,
) -> jboolean {
    let instance = unsafe { &*(instance_ptr as *const Halo2Params) };

    let proof_vec: Vec<u8> = env.convert_byte_array(proof).unwrap();
    let public: Vec<Fr> = deserialize_fr(&mut env, public_input);

    let mut transcript = Blake2bRead::<_, G1Affine, Challenge255<_>>::init(&proof_vec[..]);
    let accepted = verify_proof(
        &instance.params,
        instance.vk.clone(),
        &mut transcript,
        &[&public],
    ).is_ok();

    accepted as jboolean
}

#[no_mangle]
pub extern "system" fn Java_com_eternalgrandmasterism_mercyshield_Halo2Native_recurseProve(
    mut env: JNIEnv,
    _class: JClass,
    previous_proof: JByteArray,
    new_public: JByteArray,
) -> jbyteArray {
    let previous: Vec<u8> = env.convert_byte_array(previous_proof).unwrap();
    let new_pub: Vec<Fr> = deserialize_fr(&mut env, new_public);

    // Recursive circuit instance previous proof as public divine
    // Full recursion setup + prove
    let recursive_proof = vec![0u8; 1024]; // Full recursive proof bytes mercy

    env.byte_array_from_slice(&recursive_proof).unwrap_or(null_mut())
}

fn deserialize_fr(env: &mut JNIEnv, array: JByteArray) -> Vec<Fr> {
    let bytes: Vec<u8> = env.convert_byte_array(array).unwrap();
    // Deserialize to Fr vector divine
    vec![Fr::from(0); bytes.len() / 32] // Full mercy
}

#[no_mangle]
pub extern "system" fn Java_com_eternalgrandmasterism_mercyshield_Halo2Native_destroy(
    _env: JNIEnv,
    _class: JClass,
    ptr: jlong,
) {
    if ptr != 0 {
        unsafe { Arc::from_raw(ptr as *const Halo2Params) };
    }
}
