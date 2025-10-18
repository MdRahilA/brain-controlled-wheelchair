# software/ui/calibrate.py
"""
Minimal calibration / live-scores UI for SSVEP.
- Plots the CCA scores for your target frequencies every update.
- Shows predicted command (after simple mapping + dwell/confidence gating).
- Uses synthetic EEG for now (so you can test end-to-end). Replace `get_eeg_window()`
  with real EEG streaming later (LSL/device SDK).

Controls:
- Close the matplotlib window or press Ctrl+C in terminal to stop.
"""

import time
import numpy as np
import matplotlib.pyplot as plt

from preprocessing.filters import preprocess_window
from features.ssvep_cca import classify_window
from control.controller import Controller, Cmd, freq_to_cmd

# ---------------- Config ---------------- #
FS = 250               # sampling rate
WIN_SEC = 2.0          # window length
TARGETS = (8, 12, 15)  # SSVEP flicker frequencies
MAINS_HZ = 50.0        # notch mains
CONF_THRESH = 0.65     # controller confidence threshold
DWELL_SEC = 1.0        # controller dwell time
SYN_NOISE = 0.6        # synthetic EEG noise amplitude

# -------------- Synthetic EEG -------------- #
def get_eeg_window(ch=4, n=None, true_freq=None, noise=SYN_NOISE):
    """
    Replace this with real EEG:
      - Pull a (channels x samples) window from LSL/device SDK
      - Sample rate should be FS
    """
    n = n or int(FS * WIN_SEC)
    f = float(true_freq if true_freq is not None else np.random.choice(TARGETS))
    t = np.arange(n) / FS
    sig = np.sin(2 * np.pi * f * t)[None, :]     # 1 x n
    sig = np.repeat(sig, ch, axis=0)             # ch x n
    return sig + noise * np.random.randn(ch, n), f

# -------------- Main loop -------------- #
def main():
    ctrl = Controller(dwell=DWELL_SEC, conf_threshold=CONF_THRESH)

    # Matplotlib bar plot setup
    plt.ion()
    fig, ax = plt.subplots()
    bars = ax.bar([str(f) for f in TARGETS], [0]*len(TARGETS))
    ax.set_ylim(0, 1.5)
    ax.set_ylabel("CCA score")
    ax.set_title("SSVEP Live Scores")

    text_pred = ax.text(0.02, 0.95, "Pred: -", transform=ax.transAxes, fontsize=12, va="top")
    text_cmd  = ax.text(0.02, 0.88, "Cmd: STOP", transform=ax.transAxes, fontsize=12, va="top")
    text_info = ax.text(0.02, 0.81, "Info: synthetic EEG", transform=ax.transAxes, fontsize=10, va="top", color="gray")

    try:
        while plt.fignum_exists(fig.number):
            # --- Get EEG window (synthetic for now) ---
            eeg_win, true_f = get_eeg_window()

            # --- Preprocess ---
            x = preprocess_window(eeg_win, fs=FS, mains=MAINS_HZ, bp_low=1.0, bp_high=40.0, do_zscore=True)

            # --- Classify ---
            pred_f, conf, scores = classify_window(x, FS, targets=TARGETS)
            candidate_cmd = freq_to_cmd(pred_f)

            # For now, no sensor block in this UI
            final_cmd = ctrl.step(candidate_cmd=candidate_cmd, confidence=conf, safety_blocked=False)

            # --- Update plot ---
            score_vals = [scores[f] for f in TARGETS]
            max_score = max(1.5, max(score_vals) + 0.1)
            ax.set_ylim(0, max_score)
            for b, v in zip(bars, score_vals):
                b.set_height(v)

            text_pred.set_text(f"Pred: {pred_f:.0f} Hz (true={true_f:.0f} Hz), conf≈{conf:.3f}")
            text_cmd.set_text(f"Cmd: {final_cmd.value if isinstance(final_cmd, Cmd) else final_cmd}")

            plt.pause(0.05)  # yield to UI loop

            # Slow down updates slightly so it’s readable
            time.sleep(0.25)

    except KeyboardInterrupt:
        pass
    finally:
        try:
            plt.ioff()
            plt.close(fig)
        except Exception:
            pass

if __name__ == "__main__":
    main()
