import numpy as np
import json
import hashlib

# 8x8 Grid for the reverse entropy challenge
GRID_SIZE = 8

def step_game_of_life(grid):
    """Executes 1 generation step of Conway's Game of Life."""
    neighbors = sum(np.roll(np.roll(grid, i, 0), j, 1)
                    for i in (-1, 0, 1) for j in (-1, 0, 1)
                    if (i, j) != (0, 0))
    return (neighbors == 3) | (grid & (neighbors == 2))

# Secret Seed (S_0) - Hidden from solvers
# Generated deterministically using the "14.0" key from Phase 002
np.random.seed(140)
S_0 = np.random.choice([0, 1], size=(GRID_SIZE, GRID_SIZE), p=[0.7, 0.3])

# Advance to Generation 50 (S_50)
S_50 = S_0.copy()
for _ in range(50):
    S_50 = step_game_of_life(S_50)

# Generate Hash of S_0 for verification without spoiling answer
s0_str = "".join(map(str, S_0.flatten()))
s0_hash = hashlib.sha256(s0_str.encode()).hexdigest()

challenge_payload = {
    "phase": "003",
    "title": "REVERSE ENTROPY GATE",
    "grid_dimensions": [GRID_SIZE, GRID_SIZE],
    "generations_forward": 50,
    "target_state_S50": S_50.tolist(),
    "verification_sha256": s0_hash,
    "instruction": "Determine the unique initial state S_0. Submit S_0 as a flat 64-character binary string."
}

with open("phase003_challenge.json", "w") as f:
    json.dump(challenge_payload, f, indent=4)

print("[+] Generated phase003_challenge.json")
print(f"[+] S_50 Active Cells: {int(np.sum(S_50))}")
print(f"[+] Proof Verification Hash: {s0_hash[:16]}...")
