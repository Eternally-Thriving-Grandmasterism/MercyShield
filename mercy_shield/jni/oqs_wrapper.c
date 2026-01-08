#include <jni.h>
#include <oqs/oqs.h>
#include <string.h>
#include <stdlib.h>

JNIEXPORT jbyteArray JNICALL Java_com_eternalgrandmasterism_mercyshield_PQCNative_kemKeygen(JNIEnv *env, jclass clazz) {
    OQS_KEM *kem = OQS_KEM_new(OQS_KEM_alg_kyber_768);
    if (!kem) return NULL;

    uint8_t *pk = malloc(kem->length_public_key);
    uint8_t *sk = malloc(kem->length_secret_key);
    OQS_KEM_keypair(kem, pk, sk);

    jbyteArray result = (*env)->NewByteArray(env, kem->length_public_key + kem->length_secret_key);
    (*env)->SetByteArrayRegion(env, result, 0, kem->length_public_key, (jbyte*)pk);
    (*env)->SetByteArrayRegion(env, result, kem->length_public_key, kem->length_secret_key, (jbyte*)sk);

    free(pk); free(sk);
    OQS_KEM_free(kem);
    return result;
}

JNIEXPORT jbyteArray JNICALL Java_com_eternalgrandmasterism_mercyshield_PQCNative_kemEncaps(JNIEnv *env, jclass clazz, jbyteArray jpk) {
    jbyte *pk = (*env)->GetByteArrayElements(env, jpk, NULL);
    size_t pk_len = (*env)->GetArrayLength(env, jpk);

    OQS_KEM *kem = OQS_KEM_new(OQS_KEM_alg_kyber_768);
    uint8_t *ct = malloc(kem->length_ciphertext);
    uint8_t *ss = malloc(kem->length_shared_secret);
    OQS_KEM_encaps(kem, ct, ss, pk);

    jbyteArray result = (*env)->NewByteArray(env, kem->length_ciphertext + kem->length_shared_secret);
    (*env)->SetByteArrayRegion(env, result, 0, kem->length_ciphertext, (jbyte*)ct);
    (*env)->SetByteArrayRegion(env, result, kem->length_ciphertext, kem->length_shared_secret, (jbyte*)ss);

    free(ct); free(ss);
    (*env)->ReleaseByteArrayElements(env, jpk, pk, JNI_ABORT);
    OQS_KEM_free(kem);
    return result;
}

// Similar for decaps, dsa keygen/sign/verify divine full

// Error handling expand mercy
