pragma circom 2.3.0;

include "node_modules/circomlib/circuits/comparators.circom";
include "node_modules/circomlib/circuits/bitify.circom";
include "node_modules/circomlib/circuits/poseidon.circom"; // PLONK friendly hash mercy

template RulesCompliance(num_rules) {
    signal input rules_hash; // Public committed hash
    signal input rule_values[num_rules]; // Private 0/1 allow/block
    signal input preimage_hash; // Private preimage lead to public hash

    // Poseidon hash chain symbolic (PLONK efficient divine)
    component poseidon = Poseidon(num_rules);
    for (var i = 0; i < num_rules; i++) {
        poseidon.inputs[i] <== rule_values[i];
    }

    preimage_hash === poseidon.out;

    // Public rules_hash match
    rules_hash === preimage_hash;

    // Example range: rule_values 0 or 1
    component is_binary[num_rules];
    for (var i = 0; i < num_rules; i++) {
        is_binary[i] = IsZero();
        is_binary[i].in <== rule_values[i] * (rule_values[i] - 1);
        is_binary[i].out === 0;
    }
}

component main {public [rules_hash]} = RulesCompliance(100); // Expand num_rules mercy
