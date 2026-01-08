// src/lib.rs - Halo2 Native Integration ∞ Pure
// cdylib C ABI - direct call from Python via ctypes

#![feature(once_cell)]

use halo2_proofs::dev::MockProver;
use halo2_proofs::pasta::Fp;
use halo2_proofs::circuit::Value;

mod circuits;

use circuits::range_check::RangeCheckCircuit;

#[no_mangle]
pub extern "C" fn halo2_check_range64(value: u64) -> u8 {
    let v = Fp::from(value);

    let circuit = RangeCheckCircuit {
        value: Value::known(v),
    };

    let prover = MockProver::run(9, &circuit, vec![]).map_err(|_| ()) .unwrap_or_else(|_| return 0);

    if prover.verify().is_ok() {
        1u8 // Harmony Pure - value in strict range
    } else {
        0u8 // Shadow - overflow or bad, trigger mercy
    }
}
