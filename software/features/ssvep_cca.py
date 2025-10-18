# software/features/ssvep_cca.py
import numpy as np

def _ref(freq: float, fs: float, n_samples: int) -> np.ndarray:
    """Generate sine/cosine reference signals for CCA at fundamental & harmonic frequencies."""
    t = np.arange(n_samples) / fs
    return np.vstack([
        np.sin(2*np.pi*freq*t), np.cos(2*np.pi*freq*t),
        np.sin(4*np.pi*freq*t), np.cos(4*np.pi*freq*t)
    ])

def _cca_score(X: np.ndarray, Y: np.ndarray) -> float:
    """Compute canonical correlation between EEG and reference signals."""
    Sxx = X @ X.T + 1e-6*np.eye(X.shape[0])
    Syy = Y @ Y.T + 1e-6*np.eye(Y.shape[0])
    Sxy = X @ Y.T
    M = np.linalg.pinv(Sxx) @ Sxy @ np.linalg.pinv(Syy) @ Sxy.T
    vals = np.linalg.eigvals(M)
    return float(np.sqrt(np.max(np.real(vals))))

def classify_window(eeg_win: np.ndarray, fs: float, targets=(8, 12, 15)):
    """
    Classify a short EEG window using CCA across multiple target frequencies.
    Returns: (predicted_frequency, confidence_score, all_scores)
    """
    scores = {f: _cca_score(eeg_win, _ref(f, fs, eeg_win.shape[1])) for f in targets}
    f_star, s_star = max(scores.items(), key=lambda kv: kv[1])
    return f_star, s_star, scores
