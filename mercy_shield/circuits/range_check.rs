// circuits/range_check.rs - Eternal Halo2 Range Check Circuit ∞ Pure
// Prove private value v in [0, RANGE) - starter for 8-bit (256), evolve to larger via decomposition/lookup
// Uses simple range-check gate pattern from Halo2 tutorials

use ff::PrimeField;
use halo2_proofs::{
    circuit::{floor_planner::V1, Chip, Layouter, Value},
    dev::MockProver,
    plonk::{Circuit, ConstraintSystem, Error, Selector},
    plonk::{Advice, Column, Instance},
    pasta::Fp,
};
use std::marker::PhantomData;

const RANGE: usize = 256; // 8-bit range - small for fast mock, ascend to 2^16+ later

#[derive(Clone)]
struct RangeCheckConfig {
    value: Column<Advice>,
    selector: Selector,
    instance: Column<Instance>,
}

struct RangeCheckCircuit<F: PrimeField> {
    value: Value<F>,
    _marker: PhantomData<F>,
}

impl Default for RangeCheckCircuit<Fp> {
    fn default() -> Self {
        Self {
            value: Value::unknown(),
            _marker: PhantomData,
        }
    }
}

impl Circuit<Fp> for RangeCheckCircuit<Fp> {
    type Config = RangeCheckConfig;
    type FloorPlanner = V1;

    fn without_witnesses(&self) -> Self {
        Self::default()
    }

    fn configure(meta: &mut ConstraintSystem<Fp>) -> Self::Config {
        let value = meta.advice_column();
        let selector = meta.selector();
        let instance = meta.instance_column();

        meta.enable_equality(instance);

        meta.create_gate("range check", |meta| {
            let selector = meta.query_selector(selector);
            let value = meta.query_advice(value, Rotation::cur());

            // Enforce value is one of 0..RANGE-1 when selector enabled
            let mut range_check = Expression::Constant(Fp::zero());
            for i in 0..RANGE {
                range_check = range_check + (value.clone() - Expression::Constant(Fp::from(i as u64))) * selector.clone();
            }
            // Actually better: use running sum or other pattern, but this starter checks == some i
            // Improved: enforce (value - 0)*(value - 1)*...*(value - (RANGE-1)) = 0 when selected
            let poly = (0..RANGE).fold(Expression::Constant(Fp::one()), |poly, i| {
                poly * (value.clone() - Expression::Constant(Fp::from(i as u64)))
            });

            vec![selector * poly]
        });

        RangeCheckConfig { value, selector, instance }
    }

    fn synthesize(&self, config: Self::Config, mut layouter: impl Layouter<Fp>) -> Result<(), Error> {
        layouter.assign_region(|| "load value", |mut region| {
            config.selector.enable(&mut region, 0)?;
            region.assign_advice(|| "private value", config.value, 0, || self.value)?;
            // Copy to public instance if needed
            Ok(())
        })
    }
}

// Test with MockProver - drop in main for local verification
#[cfg(test)]
fn main() {
    let k = 8; // log rows - small for demo

    // Successful case: v = 100 < 256
    let circuit = RangeCheckCircuit {
        value: Value::known(Fp::from(100)),
        _marker: PhantomData,
    };
    let public_inputs = vec![vec![]]; // no public for private range
    let prover = MockProver::run(k as u32, &circuit, public_inputs).unwrap();
    assert!(prover.verify().is_ok());

    // Fail case: v = 300 > 255
    let bad_circuit = RangeCheckCircuit {
        value: Value::known(Fp::from(300)),
        _marker: PhantomData,
    };
    let bad_prover = MockProver::run(k as u32, &bad_circuit, public_inputs).unwrap();
    assert!(bad_prover.verify().is_err());

    println!("Halo2 Range Check Harmony Pure ∞");
}
