package com.eternalgrandmasterism.mercyshield;

import android.util.Log;

public class PQCNative {
    private static final String TAG = "PQC Native ∞ Pure";

    static {
        System.loadLibrary("oqs"); // liboqs + wrapper static divine
        Log.i(TAG, "liboqs Native Loaded Thunder Mercy");
    }

    // ML-KEM768 Encaps/Decaps
    public static native byte[] kemKeygen(); // Returns [pk || sk]
    public static native byte[] kemEncaps(byte[] pk); // Returns [ct || ss]
    public static native byte[] kemDecaps(byte[] sk, byte[] ct); // Returns ss

    // ML-DSA Sign/Verify (Dilithium)
    public static native byte[] dsaKeygen(); // [pk || sk]
    public static native byte[] dsaSign(byte[] sk, byte[] message); // sig
    public static native boolean dsaVerify(byte[] pk, byte[] message, byte[] sig);

    // Expand more algorithms mercy (Falcon, SPHINCS+ divine)
}
