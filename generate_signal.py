import numpy as np
import scipy.io.wavfile as wav

# Audio parameters
sample_rate = 44100  # 44.1 kHz standard audio
duration_per_char = 0.35  # seconds per character column
base_freq = 2000     # Base frequency in Hz
freq_step = 200      # Distance between vertical pixels

# The hidden spectrogram message matrix (8 rows high)
# 1 = Tone present, 0 = Silence
CHAR_MAP = {
    'A': [
        [0,1,1,1,0],
        [1,0,0,0,1],
        [1,1,1,1,1],
        [1,0,0,0,1],
        [1,0,0,0,1]
    ],
    'P': [
        [1,1,1,1,0],
        [1,0,0,0,1],
        [1,1,1,1,0],
        [1,0,0,0,0],
        [1,0,0,0,0]
    ],
    'H': [
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,1,1,1,1],
        [1,0,0,0,1],
        [1,0,0,0,1]
    ],
    'E': [
        [1,1,1,1,1],
        [1,0,0,0,0],
        [1,1,1,1,0],
        [1,0,0,0,0],
        [1,1,1,1,1]
    ],
    'L': [
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,1,1,1,1]
    ],
    'I': [
        [1,1,1],
        [0,1,0],
        [0,1,0],
        [0,1,0],
        [1,1,1]
    ],
    'O': [
        [0,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [0,1,1,1,0]
    ],
    'N': [
        [1,0,0,0,1],
        [1,1,0,0,1],
        [1,0,1,0,1],
        [1,0,0,1,1],
        [1,0,0,0,1]
    ],
    ' ': [
        [0,0],
        [0,0],
        [0,0],
        [0,0],
        [0,0]
    ],
    '-': [
        [0,0,0],
        [0,0,0],
        [1,1,1],
        [0,0,0],
        [0,0,0]
    ],
    '1': [
        [0,1,0],
        [1,1,0],
        [0,1,0],
        [0,1,0],
        [1,1,1]
    ],
    '4': [
        [1,0,1],
        [1,0,1],
        [1,1,1],
        [0,0,1],
        [0,0,1]
    ],
    '0': [
        [0,1,1,0],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [0,1,1,0]
    ],
    '.': [
        [0],
        [0],
        [0],
        [0],
        [1]
    ]
}

def render_spectrogram_text(text):
    columns = []
    
    # Assemble bitmap columns
    for char in text.upper():
        if char in CHAR_MAP:
            matrix = CHAR_MAP[char]
            cols = len(matrix[0])
            for c in range(cols):
                col_pixels = [matrix[r][c] for r in range(len(matrix))]
                columns.append(col_pixels)
            # Spacing column between letters
            columns.append([0]*len(matrix))

    total_audio = np.array([], dtype=np.float32)
    t_col = np.linspace(0, duration_per_char, int(sample_rate * duration_per_char), endpoint=False)

    for col in columns:
        col_signal = np.zeros_like(t_col)
        # Flip vertically so top of letter is higher frequency
        for row_idx, val in enumerate(reversed(col)):
            if val == 1:
                freq = base_freq + (row_idx * freq_step)
                col_signal += np.sin(2 * np.pi * freq * t_col)
        
        # Normalize signal amplitude per column
        if np.max(np.abs(col_signal)) > 0:
            col_signal = col_signal / np.max(np.abs(col_signal)) * 0.5
            
        total_audio = np.concatenate((total_audio, col_signal))

    # Convert to 16-bit PCM format
    audio_int16 = (total_audio * 32767).astype(np.int16)
    wav.write("signal_002.wav", sample_rate, audio_int16)
    print("[+] Audio file generated: signal_002.wav")

if __name__ == "__main__":
    render_spectrogram_text("APHELION 14.0")
