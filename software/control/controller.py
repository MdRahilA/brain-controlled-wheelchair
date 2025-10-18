# software/control/controller.py
# Converts noisy predictions into safe, debounced commands.

import time
from enum import Enum

class Cmd(Enum):
    STOP = "STOP"
    FWD  = "FWD"
    LEFT = "LEFT"
    RIGHT= "RIGHT"

class Controller:
    """
    Debounce + dwell + confidence gating + safety override.
    - If safety_blocked is True -> always STOP.
    - Require the same candidate for 'dwell' seconds AND confidence >= threshold.
    - Otherwise output STOP (dead-man style).
    """
    def __init__(self, dwell: float = 1.0, conf_threshold: float = 0.7):
        self.dwell = float(dwell)
        self.conf_threshold = float(conf_threshold)
        self._held_cmd: Cmd | None = None
        self._t0: float | None = None

    def reset(self):
        self._held_cmd, self._t0 = None, None

    def step(self, candidate_cmd: Cmd, confidence: float, safety_blocked: bool) -> Cmd:
        # Safety layer overrides everything
        if safety_blocked:
            self.reset()
            return Cmd.STOP

        # If confidence is too low -> hold/STOP
        if confidence < self.conf_threshold:
            self.reset()
            return Cmd.STOP

        # Debounce/dwell logic
        now = time.time()
        if candidate_cmd != self._held_cmd:
            # New candidate: start dwell timer
            self._held_cmd = candidate_cmd
            self._t0 = now
            return Cmd.STOP  # wait dwell time before acting

        # Same candidate; check dwell time
        if self._t0 is None or (now - self._t0) < self.dwell:
            return Cmd.STOP

        # Passed dwell & confidence: emit command
        return self._held_cmd or Cmd.STOP


def freq_to_cmd(freq_hz: float) -> Cmd:
    """
    Map SSVEP target frequency to a command.
    Adjust this mapping to match the flicker UI you use.
    """
    # Example mapping (edit if your targets differ)
    if abs(freq_hz - 8) <= 0.5:
        return Cmd.LEFT
    if abs(freq_hz - 12) <= 0.5:
        return Cmd.FWD
    if abs(freq_hz - 15) <= 0.5:
        return Cmd.RIGHT
    return Cmd.STOP
