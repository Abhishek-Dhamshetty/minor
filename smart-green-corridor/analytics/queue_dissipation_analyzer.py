"""Analyzes queue dissipation after preemption."""
class QueueDissipationAnalyzer:
    def compute(self, queues: list[int]) -> float:
        return sum(queues) / max(1, len(queues))
