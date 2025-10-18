# software/sensors/safety_layer.py
"""
Basic safety layer for obstacle avoidance.

Usage:
    sl = SafetyLayer(stop_distance_cm=60)
    sl.update(distances_cm={"front": 45, "left": 120, "right": 95})
    blocked = sl.is_blocked()              # -> True if any sensor < threshold
    blocked_front = sl.blocked_reason()    # -> "front" (or None)

You can feed real sensor data from your MCU (over serial) or mock values during testing.
"""

from __future__ import annotations
from typing import Dict, Optional

class SafetyLayer:
    def __init__(self, stop_distance_cm: float = 60.0):
        """
        stop_distance_cm: distance below which motion should be blocked.
        """
        self.stop_distance_cm = float(stop_distance_cm)
        self._distances_cm: Dict[str, float] = {}
        self._last_blocked_key: Optional[str] = None

    def update(self, distances_cm: Dict[str, float]) -> None:
        """
        distances_cm example:
            {"front": 45.0, "left": 120.0, "right": 95.0, "rear": 200.0}
        """
        self._distances_cm = dict(distances_cm or {})
        self._last_blocked_key = None
        for k, d in self._distances_cm.items():
            try:
                if float(d) < self.stop_distance_cm:
                    self._last_blocked_key = k
                    break
            except (TypeError, ValueError):
                # Ignore bad readings
                continue

    def is_blocked(self) -> bool:
        """True if any sensor reports distance below threshold."""
        return self._last_blocked_key is not None

    def blocked_reason(self) -> Optional[str]:
        """Returns the sensor name that triggered the block, or None."""
        return self._last_blocked_key

    def set_threshold(self, stop_distance_cm: float) -> None:
        self.stop_distance_cm = float(stop_distance_cm)
