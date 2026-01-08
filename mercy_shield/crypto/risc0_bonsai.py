import requests
import logging
import os
from typing import List, Tuple

BONSAI_API_URL = "https://api.bonsai.xyz/v1/prove"
BONSAI_API_KEY = ""  # Your key

PROOF_DIR = "/sdcard/MercyShield/zkvm_proofs/"

def bonsai_prove_aggregated_cloud(image_id: str, values: List[int]) -> bytes:
    if not image_id:
        logging.warning("Bonsai Image ID Missing")
        return b''

    os.makedirs(PROOF_DIR, exist_ok=True)

    input_bytes = b''.join(v.to_bytes(8, 'big') for v in values)
    payload = {
        "image_id": image_id,
        "input": input_bytes.hex(),
    }

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": BONSAI_API_KEY
    }

    try:
        response = requests.post(BONSAI_API_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "SUCCESS":
            receipt_hex = data.get("receipt", "")
            receipt = bytes.fromhex(receipt_hex)
            receipt_path = os.path.join(PROOF_DIR, f"aggreg_receipt_{int(os.time())}.bin")
            with open(receipt_path, 'wb') as f:
                f.write(receipt)
            logging.info(f"Bonsai Aggreg Receipt Saved: {receipt_path}")
            return receipt
        else:
            logging.warning(f"Bonsai Status Error: {data}")
            return b''
    except requests.Timeout:
        logging.error("Bonsai Timeout")
        return b''
    except Exception as e:
        logging.error(f"Bonsai Cloud Error: {e}")
        return b''

def bonsai_verify_local(receipt_bytes: bytes, expected_num: int = 16) -> Tuple[bool, List[int], List[str]]:
    try:
        if len(receipt_bytes) < expected_num * (4 + 32):
            return False, [], ["Receipt Too Short"]

        flags = []
        offset = 0
        for i in range(expected_num):
            flag = int.from_bytes(receipt_bytes[offset:offset+4], 'big')
            flags.append(flag)
            offset += 4

        if not all(f == 1 for f in flags):
            return False, flags, ["Not All Junctions Proven Safe"]

        hashes = []
        for i in range(expected_num):
            h = receipt_bytes[offset:offset+32].hex()
            hashes.append(h)
            offset += 32

        return True, flags, hashes
    except Exception as e:
        logging.error(f"Local Verify Error: {e}")
        return False, [], [str(e)]
