#![no_std]
#![no_main]

use risc0_zkvm::guest::env;
use risc0_zkvm::sha::Digest;

risc0_zkvm::entry!(main);

const NUM_VALUES: usize = 8;  // Aggregated vector size — adjust for lattice (8-32 mercy)
const MAX_SAFE: u64 = 18_446_744_073_709_551_615;  // u64::MAX mercy bound

pub fn main() {
    // Read aggregated private anomaly vector from host (NUM_VALUES u64)
    let mut values: [u64; NUM_VALUES] = [0; NUM_VALUES];
    for i in 0..NUM_VALUES {
        values[i] = env::read();
    }

    // Proven flags array — 1 safe each
    let mut flags: [u32; NUM_VALUES] = [0; NUM_VALUES];

    // Hidden hashes array
    let mut hashes: [Digest; NUM_VALUES] = [Digest::default(); NUM_VALUES];

    for i in 0..NUM_VALUES {
        let v = values[i];

        if v >= MAX_SAFE {
            panic!("Aggregated Shadow Critical — No Proof on Bad Value ∞");
        }

        flags[i] = 1;  // Proven safe

        let v_bytes = v.to_be_bytes();
        hashes[i] = risc0_zkvm::sha::digest_u8_slice(&v_bytes);
    }

    // Public journal commits — verifier reads proven flags + hidden hashes
    env::commit(&flags);
    env::commit(&hashes);
}
