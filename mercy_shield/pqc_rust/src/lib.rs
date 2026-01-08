use pyo3::prelude::*;
use pyo3::types::PyList;
use ml_kem::{MlKem768, KemCore};
use ml_dsa::MlDsa65;
use rand::thread_rng;

#[pyfunction]
fn keygen_enc() -> PyResult<(Vec<u8>, Vec<u8>)> {
    let mut rng = thread_rng();
    let (pk, sk) = MlKem768::generate(&mut rng)?;
    Ok((pk.to_bytes().to_vec(), sk.to_bytes().to_vec()))
}

#[pyfunction]
fn encaps(pk: &PyList) -> PyResult<(Vec<u8>, Vec<u8>)> {
    let pk_bytes: Vec<u8> = pk.extract()?;
    let pk = MlKem768Pk::from_bytes(&pk_bytes.try_into().map_err(|_| pyo3::exceptions::PyValueError::new_err("Invalid PK"))?);
    let mut rng = thread_rng();
    let (ct, ss) = MlKem768::encapsulate(&pk, &mut rng)?;
    Ok((ct.to_bytes().to_vec(), ss.to_bytes().to_vec()))
}

#[pyfunction]
fn decaps(sk: &PyList, ct: &PyList) -> PyResult<Vec<u8>> {
    let sk_bytes: Vec<u8> = sk.extract()?;
    let ct_bytes: Vec<u8> = ct.extract()?;
    let sk = MlKem768Sk::from_bytes(&sk_bytes.try_into().map_err(|_| pyo3::exceptions::PyValueError::new_err("Invalid SK"))?);
    let ct = MlKem768Ct::from_bytes(&ct_bytes.try_into().map_err(|_| pyo3::exceptions::PyValueError::new_err("Invalid CT"))?);
    let ss = MlKem768::decapsulate(&sk, &ct)?;
    Ok(ss.to_bytes().to_vec())
}

#[pyfunction]
fn keygen_sig() -> PyResult<(Vec<u8>, Vec<u8>)> {
    let mut rng = thread_rng();
    let (pk, sk) = MlDsa65::generate(&mut rng)?;
    Ok((pk.to_bytes().to_vec(), sk.to_bytes().to_vec()))
}

#[pyfunction]
fn sign(sk: &PyList, msg: &PyList) -> PyResult<Vec<u8>> {
    let sk_bytes: Vec<u8> = sk.extract()?;
    let msg_bytes: Vec<u8> = msg.extract()?;
    let sk = MlDsa65Sk::from_bytes(&sk_bytes.try_into().map_err(|_| pyo3::exceptions::PyValueError::new_err("Invalid SK"))?);
    let sig = MlDsa65::sign(&sk, &msg_bytes)?;
    Ok(sig.to_bytes().to_vec())
}

#[pyfunction]
fn verify(pk: &PyList, msg: &PyList, sig: &PyList) -> PyResult<bool> {
    let pk_bytes: Vec<u8> = pk.extract()?;
    let msg_bytes: Vec<u8> = msg.extract()?;
    let sig_bytes: Vec<u8> = sig.extract()?;
    let pk = MlDsa65Pk::from_bytes(&pk_bytes.try_into().map_err(|_| pyo3::exceptions::PyValueError::new_err("Invalid PK"))?);
    let sig = MlDsa65Sig::from_bytes(&sig_bytes.try_into().map_err(|_| pyo3::exceptions::PyValueError::new_err("Invalid Sig"))?);
    Ok(MlDsa65::verify(&pk, &msg_bytes, &sig).is_ok())
}

#[pymodule]
fn mercyshield_pqc(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(keygen_enc, m)?)?;
    m.add_function(wrap_pyfunction!(encaps, m)?)?;
    m.add_function(wrap_pyfunction!(decaps, m)?)?;
    m.add_function(wrap_pyfunction!(keygen_sig, m)?)?;
    m.add_function(wrap_pyfunction!(sign, m)?)?;
    m.add_function(wrap_pyfunction!(verify, m)?)?;
    Ok(())
}
