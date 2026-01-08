pragma circom 2.0.0;

include "node_modules/circomlib/circuits/sha256/sha256.circom";

template HashPreimage() {
    signal input preimage[256]; // Bit array preimage mercy
    signal input hash[256]; // Expected hash bits

    component sha256 = Sha256(256);
    for (var i = 0; i < 256; i++) {
        sha256.in[i] <== preimage[i];
    }

    for (var i = 0; i < 256; i++) {
        sha256.out[i] === hash[i];
    }
}

component main {public [hash]} = HashPreimage();
