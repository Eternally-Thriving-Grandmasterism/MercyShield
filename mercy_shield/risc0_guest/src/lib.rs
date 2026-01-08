#![no_std]
#![no_main]

use risc0_zkvm::guest::env;
use risc0_zkvm::sha::Digest;

risc0_zkvm::entry!(main);

pub fn main() {
    // Read private anomaly score from host
    let value: u64 = env::read();

    // Mercy bound — adjust for your lattice safe max
    const MAX_SAFE: u64 = 18_446_744_073_709_551_615;  // u64::MAX margin example

    // If shadow, panic — no proof generated (proven safe if receipt exists)
    if value >= MAX_SAFE {
        panic!("Range Shadow — Mercy Burst Critical ∞");
    }

    let flag: u32 = 1;  // Proven safe

    // Hide value — commit hash
    let value_bytes = value.to_be_bytes();
    let value_hash: Digest = risc0_zkvm::sha::digest_u8_slice(&value_bytes);

    // Public journal — verifier reads proven flag + hidden hash
    env::commit(&flag);
    env::commit(&value_hash);
}
