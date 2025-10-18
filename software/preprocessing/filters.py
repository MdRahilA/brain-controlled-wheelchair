# software/preprocessing/filters.py
"""
EEG preprocessing utilities:
- DC removal
- Notch filter (50/60 Hz)
- Band-pass filter (e.g., 1–40 Hz)
- Simple z-score normalization
- Convenience pipeline
"""

from __future__ import annotations
import numpy as np
from scipy.signal import iirnotch, butter, filtfilt

def remove_dc(eeg: np.ndarray) -> np.ndarray:
    """
    Subtracts channel-wise mean.
    eeg: (channels, samples)
    """
    return eeg - eeg.mean(axis=1, keepdims=True)

def notch_filter(eeg: np.ndarray, fs: float, freq: float = 50.0, q: float = 30.0) -> np.ndarray:
    """
    IIR notch to remove mains hum (50 or 60 Hz).
    q: quality factor (higher = narrower notch)
    """
    b, a = iirnotch(w0=freq/(fs/2), Q=q)
    return filtfilt(b, a, eeg, axis=1)

def bandpass(eeg: np.ndarray, fs: float, low: float = 1.0, high: float = 40.0, order: int = 4) -> np.ndarray:
    """
    Zero-phase Butterworth band-pass.
    """
    low_nyq  = low / (fs/2.0)
    high_nyq = high / (fs/2.0)
    b, a = butter(order, [low_nyq, high_nyq], btype="bandpass")
    return filtfilt(b, a, eeg, axis=1)

def zscore(eeg: np.ndarray, eps: float = 1e-8) -> np.ndarray:
    """
    Channel-wise z-score normalization.
    """
    mu  = eeg.mean(axis=1, keepdims=True)
    std = eeg.std(axis=1, keepdims=True) + eps
    return (eeg - mu) / std

def preprocess_window(
    eeg_win: np.ndarray,
    fs: float,
    mains: float = 50.0,
    bp_low: float = 1.0,
    bp_high: float = 40.0,
    do_zscore: bool = True,
) -> np.ndarray:
    """
    Convenience pipeline for a short EEG window (channels x samples).
    Steps: DC removal -> Notch -> Band-pass -> (optional) z-score.
    """
    x = remove_dc(np.asarray(eeg_win, dtype=float))
    if mains:
        x = notch_filter(x, fs, freq=mains, q=30.0)
    x = bandpass(x, fs, low=bp_low, high=bp_high, order=4)
    if do_zscore:
        x = zscore(x)
    return x
