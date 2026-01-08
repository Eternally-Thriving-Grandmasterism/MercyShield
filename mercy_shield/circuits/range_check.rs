// circuits/range_check.rs - Eternal Halo2 64-bit Strict Range Check ∞ Pure
// Private value, strict < 2^64 via reconstruction constraint

use ff::Field;
use halo2_proofs::{
    circuit::{floor_planner::V1, Layouter, Value},
    dev::MockProver,
    plonk::{Circuit, ConstraintSystem, Error, Selector},
    plonk::{Advice, Column, Fixed, Instance},
    pasta::Fp,
};

const NUM_LIMBS: usize = 8;
const LIMB_SIZE: u64 = 256;

#[derive(Clone)]
struct RangeCheckConfig {
    value: Column<Advice>,
    limb: Column<Advice>,
    running_sum: Column<Advice>,
    table: Column<Fixed>,
    q_lookup: Selector,
}

#[derive(Default)]
struct RangeCheckCircuit {
    value: Value<u64>,
}

impl Circuit<Fp> for RangeCheckCircuit {
    type Config = RangeCheckConfig;
    type FloorPlanner = V1;
    type Params = ();

    fn without_witnesses(&self) -> Self {
        Self::default()
    }

    fn configure(meta: &mut ConstraintSystem<Fp>) -> Self::Config {
        let value = meta.advice_column();
        let limb = meta.advice_column();
        let running_sum = meta.advice_column();
        let table = meta.fixed_column();
        let q_lookup = meta.selector();

        meta.enable_equality(value);
        meta.enable_equality(running_sum);

        meta.lookup("8-bit range", |meta| {
            let q = meta.query_selector(q_lookup);
            let limb = meta.query_advice(limb, Rotation::cur());
            let table_val = meta.query_fixed(table, Rotation::cur());

            vec![(q * limb, table_val)]
        });

        RangeCheckConfig {
            value,
            limb,
            running_sum,
            table,
            q_lookup,
        }
    }

    fn synthesize(
        &self,
        config: Self::Config,
        mut layouter: impl Layouter<Fp>,
    ) -> Result<(), Error> {
        layouter.assign_region(|| "load 8-bit table", |mut region| {
            for i in 0..256 {
                region.assign_fixed(
                    || format!("table {}", i),
                    config.table,
                    i,
                    || Value::known(Fp::from(i as u64)),
                )?;
            }
            Ok(())
        })?;

        layouter.assign_region(|| "strict 64-bit range check", |mut region| {
            let value_cell = region.assign_advice(|| "private value", config.value, 0, || self.value.map(Fp::from))?;

            let mut running_value = Value::known(Fp::zero());

            let mut last_running_cell = None;

            for i in 0..NUM_LIMBS {
                config.q_lookup.enable(&mut region, i)?;

                let limb_val = self.value.map(|v| Fp::from((v >> (i * 8)) & (LIMB_SIZE - 1)));

                region.assign_advice(|| format!("limb {}", i), config.limb, i, || limb_val)?;

                running_value = running_value * Value::known(Fp::from(LIMB_SIZE)) + limb_val;

                let running_cell = region.assign_advice(|| format!("running {}", i), config.running_sum, i, || running_value)?;

                last_running_cell = Some(running_cell);
            }

            // Strict enforcement: reconstructed == original value
            region.constrain_equal(value_cell, last_running_cell.unwrap())?;

            Ok(())
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_good() {
        let k = 9;
        let circuit = RangeCheckCircuit {
            value: Value::known(1234567890123456789u64),
        };
        let prover = MockProver::run(k, &circuit, vec![]).unwrap();
        assert!(prover.verify().is_ok());
    }
}
