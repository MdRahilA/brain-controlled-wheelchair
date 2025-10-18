# software/main.py
import time
import numpy as np
from features.ssvep_cca import classify_window

FS = 250          # sample rate (Hz)
WIN_SEC = 2.0     # window length (seconds)
TARGETS = (8, 12, 15)

def fake_eeg(ch=4, n=None, freq=12.0, noise=0.5):
    """Generate synthetic multi-channel EEG with a dominant SSVEP frequency."""
    n = n or int(FS * WIN_SEC)
    t = np.arange(n) / FS
    sig = np.sin(2 * np.pi * freq * t)[None, :]      # shape: (1, n)
    sig = np.repeat(sig, ch, axis=0)                 # shape: (ch, n)
    return sig + noise * np.random.randn(ch, n)

if __name__ == "__main__":
    print("Demo: SSVEP CCA on synthetic EEG. Press Ctrl+C to stop.\n")
    try:
        while True:
            # randomly pick a target frequency to simulate user focus
            true_f = float(np.random.choice(TARGETS))
            eeg_win = fake_eeg(n=int(FS * WIN_SEC), freq=true_f, noise=0.6)
            pred_f, conf, scores = classify_window(eeg_win, FS, TARGETS)
            scores_str = {k: round(v, 3) for k, v in scores.items()}
            print(f"true={true_f:.0f} Hz  pred={pred_f:.0f} Hz  conf≈{conf:.3f}  scores={scores_str}")
            time.sleep(0.6)
    except KeyboardInterrupt:
        print("\nStopped.")
