import hashlib
import json
import sys

def xor_decrypt(hex_data, key):
    key_bytes = hashlib.sha256(key.encode()).digest()
    data_bytes = bytes.fromhex(hex_data)
    return "".join([chr(b ^ key_bytes[i % len(key_bytes)]) for i, b in enumerate(data_bytes)])

def solve_phase_004():
    print("==================================================")
    print("      PROJECT APHELION // PROOF VERIFIER         ")
    print("==================================================")
    
    s0_input = input("Enter Phase 003 S_0 Flat Binary String (64 chars): ").strip()
    alias = input("Enter your Solver Handle/Alias: ").strip()

    print("\n[*] Mining dynamic proof-of-work nonce...")
    
    nonce = 0
    target = "00000"
    
    while True:
        candidate = f"{s0_input}:{alias}:{nonce}"
        proof_hash = hashlib.sha256(candidate.encode()).hexdigest()
        
        if proof_hash.startswith(target):
            print(f"[+] PROOF FOUND!")
            print(f"    Nonce: {nonce}")
            print(f"    Hash:  {proof_hash}")
            break
        nonce += 1

    # Verify and decrypt manifest
    master_key = hashlib.sha256((s0_input + "APHELION_FINAL").encode()).hexdigest()
    
    try:
        with open("manifest_payload.json", "r") as f:
            payload = json.load(f)
            
        decrypted = xor_decrypt(payload["encrypted_manifest"], master_key)
        
        if "PROJECT APHELION // UNLOCKED" in decrypted:
            print("\n" + decrypted)
        else:
            print("\n[-] Decryption Failed. The S_0 string provided is incorrect.")
    except Exception as e:
        print(f"\n[-] Error reading manifest_payload.json: {e}")

if __name__ == "__main__":
    solve_phase_004()
