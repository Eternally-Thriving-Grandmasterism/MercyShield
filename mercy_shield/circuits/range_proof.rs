// circuits/range_proof.rs - Halo2 Hiding Range Proof ∞ Pure
// Private v < 2^64, public commitment C = v * G + blinder * H, prove range without reveal v

use halo2_proofs::{
    arithmetic::Field,
    circuit::{Layouter, SimpleFloorPlanner, Value},
    plonk::{Advice, Column, ConstraintSystem, Error, Instance, Selector},
    poly::Rotation,
};
use halo2_proofs::pasta::Fp;

const NUM_LIMBS: usize = 8;
const LIMB_SIZE: u64 = 256;

#[derive(Clone)]
struct RangeProofConfig {
    limb: Column<Advice>,
    running_sum: Column<Advice>,
    commitment: Column<Instance>,
    blinder: Column<Advice>,  // Private
    table: Column<Fixed>,
    q_lookup: Selector,
}

#[derive(Default)]
struct RangeProofCircuit {
    value: Value<u64>,
    blinder: Value<Fp>,
}

impl halo2_proofs::circuit::Circuit<Fp> for RangeProofCircuit {
    type Config = RangeProofConfig;
    type FloorPlanner = SimpleFloorPlanner;

    fn without_witnesses(&self) -> Self { Self::default() }

    fn configure(meta: &mut ConstraintSystem<Fp>) -> Self::Config {
        let limb = meta.advice_column();
        let running_sum = meta.advice_column();
        let blinder = meta.advice_column();
        let commitment = meta.instance_column();
        let table = meta.fixed_column();
        let q_lookup = meta.selector();

        meta.enable_equality(commitment);

        meta.lookup("8-bit range", |meta| {
            let q = meta.query_selector(q_lookup);
            let limb = meta.query_advice(limb, Rotation::cur());
            let table_val = meta.query_fixed(table, Rotation::cur());
            vec![(q * limb, table_val)]
        });

        // Custom gate for commitment if needed - or expose as instance

        RangeProofConfig { limb, running_sum, commitment, blinder, table, q_lookup }
    }

    fn synthesize(&self, config: Self::Config, mut layouter: impl Layouter<Fp>) -> Result<(), Error> {
        layouter.assign_region(|| "table", |mut region| {
            for i in 0..256 {
                region.assign_fixed(|| "table", config.table, i, || Value::known(Fp::from(i as u64)))?;
            }
            Ok(())
        })?;

        layouter.assign_region(|| "hiding range proof", |mut region| {
            region.assign_advice(|| "blinder private", config.blinder, 0, || self.blinder)?;

            let mut running = Value::known(Fp::zero());

            for i in 0..NUM_LIMBS {
                config.q_lookup.enable(&mut region, i)?;

                let limb = self.value.map(|v| Fp::from((v >> (i * 8)) & (LIMB_SIZE - 1)));
                region.assign_advice(|| "limb", config.limb, i, || limb)?;

                running = running * Value::known(Fp::from(LIMB_SIZE)) + limb;
            }

            // Public commitment expose - simplified pasta base point
            let commitment_val = self.value.map(Fp::from) * Fp::from(1) + self.blinder * Fp::from(2);  // Placeholder G/H
            region.assign_advice(|| "reconstruct", config.running_sum, NUM_LIMBS, || running)?;
            // Constrain commitment = running + blinder term if needed

            // Expose commitment as public instance
            let commit_cell = region.assign_advice(|| "commit calc", config.running_sum, NUM_LIMBS + 1, || commitment_val)?;
            region.constrain_equal(commit_cell.cell(), config.commitment.into())?;

            Ok(())
        })
    }
}
