#![no_std]
#![no_main]

use risc0_zkvm::guest::env;
use risc0_zkvm::sha::Digest;

risc0_zkvm::entry!(main);

pub fn main() {
    // Read private anomaly score/value from host (u64)
    let value: u64 = env::read();

    // Fixed safe bound (adjust for your lattice — e.g., max safe anomaly score)
    const MAX_SAFE: u64 = 10_000_000_000_000_000_000;  // Example < 2^64 margin

    // Proven flag: 1 if safe, panic abort if shadow (no proof generated if out)
    if value >= MAX_SAFE {
        panic!("Range Shadow Critical — No Proof Generated");
    }

    let flag: u32 = 1;  // Proven safe

    // Hide value — commit SHA256(value)
    let value_bytes = value.to_be_bytes();
    let value_hash: Digest = risc0_zkvm::sha::digest_u8_slice(&value_bytes);

    // Public journal commits — verifier reads these proven
    env::commit(&flag);
    env::commit(&value_hash);
}
