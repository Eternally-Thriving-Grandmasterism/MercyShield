use pyo3::prelude::*;
use pqcrypto_kyber::kyber1024::*;
use pqcrypto_traits::kem::{Ciphertext, PublicKey, SecretKey, SharedSecret};

#[pyfunction]
fn generate_keypair() -> (Vec<u8>, Vec<u8>) {
    let (pk, sk) = keypair();
    (pk.as_bytes().to_vec(), sk.as_bytes().to_vec())
}

#[pyfunction]
fn encapsulate(pk_bytes: Vec<u8>) -> (Vec<u8>, Vec<u8>) {
    let pk = PublicKey::from_bytes(&pk_bytes).unwrap();
    let (ss, ct) = encapsulate(&pk);
    (ss.as_bytes().to_vec(), ct.as_bytes().to_vec())
}

#[pyfunction]
fn decapsulate(sk_bytes: Vec<u8>, ct_bytes: Vec<u8>) -> Vec<u8> {
    let sk = SecretKey::from_bytes(&sk_bytes).unwrap();
    let ct = Ciphertext::from_bytes(&ct_bytes).unwrap();
    let ss = decapsulate(&sk, &ct);
    ss.as_bytes().to_vec()
}

#[pymodule]
fn mercy_pqc(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate_keypair, m)?)?;
    m.add_function(wrap_pyfunction!(encapsulate, m)?)?;
    m.add_function(wrap_pyfunction!(decapsulate, m)?)?;
    Ok(())
}
