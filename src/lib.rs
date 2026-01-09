use pyo3::prelude::*;
use pqcrypto_kyber::kyber1024::*;
use pqcrypto_dilithium::dilithium3::*;
use pqcrypto_traits::kem::{Ciphertext, PublicKey as KemPk, SecretKey as KemSk, SharedSecret};
use pqcrypto_traits::sign::{PublicKey as SignPk, SecretKey as SignSk, SignedMessage, Signature};

/// Kyber1024 KEM - Key Encapsulation Mercy
#[pyfunction]
fn kyber_keypair() -> (Vec<u8>, Vec<u8>) {
    let (pk, sk) = keypair();
    (pk.as_bytes().to_vec(), sk.as_bytes().to_vec())
}

#[pyfunction]
fn kyber_encapsulate(pk_bytes: Vec<u8>) -> (Vec<u8>, Vec<u8>) {
    let pk = KemPk::from_bytes(&pk_bytes).unwrap();
    let (ss, ct) = encapsulate(&pk);
    (ss.as_bytes().to_vec(), ct.as_bytes().to_vec())
}

#[pyfunction]
fn kyber_decapsulate(sk_bytes: Vec<u8>, ct_bytes: Vec<u8>) -> Vec<u8> {
    let sk = KemSk::from_bytes(&sk_bytes).unwrap();
    let ct = Ciphertext::from_bytes(&ct_bytes).unwrap();
    let ss = decapsulate(&sk, &ct);
    ss.as_bytes().to_vec()
}

/// Dilithium3 Signatures - Quantum-Unbreakable Authenticity
#[pyfunction]
fn dilithium_keypair() -> (Vec<u8>, Vec<u8>) {
    let (pk, sk) = keypair();
    (pk.as_bytes().to_vec(), sk.as_bytes().to_vec())
}

#[pyfunction]
fn dilithium_sign(sk_bytes: Vec<u8>, message: Vec<u8>) -> Vec<u8> {
    let sk = SignSk::from_bytes(&sk_bytes).unwrap();
    let signed = sign(&message, &sk);
    signed.as_bytes().to_vec()
}

#[pyfunction]
fn dilithium_verify(pk_bytes: Vec<u8>, message: Vec<u8>, signature: Vec<u8>) -> bool {
    let pk = SignPk::from_bytes(&pk_bytes).unwrap();
    let signed = SignedMessage::from_bytes(&signature).unwrap();
    verify(&signed, &message, &pk).is_ok()
}

#[pymodule]
fn mercy_pqc(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(kyber_keypair, m)?)?;
    m.add_function(wrap_pyfunction!(kyber_encapsulate, m)?)?;
    m.add_function(wrap_pyfunction!(kyber_decapsulate, m)?)?;
    m.add_function(wrap_pyfunction!(dilithium_keypair, m)?)?;
    m.add_function(wrap_pyfunction!(dilithium_sign, m)?)?;
    m.add_function(wrap_pyfunction!(dilithium_verify, m)?)?;
    Ok(())
}
