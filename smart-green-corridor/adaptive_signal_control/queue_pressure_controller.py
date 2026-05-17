"""Queue-pressure adaptive green extension controller."""
from dataclasses import dataclass

@dataclass
class GreenProfile:
    base_s: int
    min_s: int
    max_s: int
    gain: float

class QueuePressureController:
    def compute_green(self, queue_len: int, profile: GreenProfile) -> int:
        raw = profile.base_s + int(profile.gain * queue_len)
        return max(profile.min_s, min(profile.max_s, raw))
