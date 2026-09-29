import hashlib
import json

# The Secret S_0 string derived from random seed 140
S_0_SECRET = "0001000100100000010010000000001000000100000100000000100010000000"

# Master Manifest Message
manifest_content = """
===================================================================
                  PROJECT APHELION // UNLOCKED
===================================================================

Congratulations, Traveler.

You have proven your mastery across cryptography, signal analysis,
cellular entropy, and computational rigor.

You are 1 of 1.

YOUR FINAL INSTRUCTION:
Send a PGP-encrypted message to the APHELION Master Key containing:
1. Your handle/alias
2. Your Phase 004 Nonce Proof
3. A public PGP key for return verification

"At aphelion, the distance is greatest, yet the orbit remains unbroken."

Key ID: 4096R/APHELION
===================================================================
"""

# Store manifest payload hash-encrypted using the master proof key
master_key = hashlib.sha256((S_0_SECRET + "APHELION_FINAL").encode()).hexdigest()

# Simple XOR Stream Encryption for the Manifest
def xor_encrypt(data, key):
    key_bytes = hashlib.sha256(key.encode()).digest()
    return "".join(["{:02x}".format(ord(c) ^ key_bytes[i % len(key_bytes)]) for i, c in enumerate(data)])

encrypted_manifest = xor_encrypt(manifest_content, master_key)

payload_file = {
    "protocol": "APHELION_PHASE_004",
    "difficulty_target": "00000",
    "encrypted_manifest": encrypted_manifest,
    "instruction": "Run verify_proof.py with your S_0 string and alias to compute the nonce and unlock."
}

with open("manifest_payload.json", "w") as f:
    json.dump(payload_file, f, indent=4)

print("[+] Created manifest_payload.json")
