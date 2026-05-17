"""Measures corridor efficiency and preemption impact."""
class CorridorEfficiencyMetrics:
    def compute(self, preemptions: int, clearance_s: float) -> float:
        return preemptions / max(1.0, clearance_s)
