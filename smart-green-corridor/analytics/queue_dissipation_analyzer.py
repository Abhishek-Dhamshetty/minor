"""Analyzes queue dissipation after preemption."""
from dataclasses import dataclass


@dataclass
class QueueSnapshot:
    phase_id: str
    queue_length: int
    timestamp_s: float


class QueueDissipationAnalyzer:
    def compute(self, queues: list[int]) -> float:
        return sum(queues) / max(1, len(queues))

    def peak_queue(self, queues: list[int]) -> int:
        if not queues:
            return 0
        return max(queues)

    def dissipation_rate(self, queues: list[int]) -> float:
        if len(queues) < 2:
            return 0.0
        return (queues[0] - queues[-1]) / max(1, len(queues) - 1)

    def classify(self, queues: list[int]) -> str:
        if not queues:
            return "empty"
        rate = self.dissipation_rate(queues)
        if rate >= 1.5:
            return "fast"
        if rate >= 0.5:
            return "steady"
        return "slow"

    def build_summary(self, queues: list[int]) -> dict:
        return {
            "avg": self.compute(queues),
            "peak": self.peak_queue(queues),
            "rate": self.dissipation_rate(queues),
            "class": self.classify(queues),
        }


def fake_queue_series(length: int = 10, start: int = 12) -> list[int]:
    queues = []
    current = max(0, start)
    for _ in range(max(0, length)):
        queues.append(current)
        current = max(0, current - 1)
    return queues


def fake_snapshots(phase_id: str, length: int = 8) -> list[QueueSnapshot]:
    queues = fake_queue_series(length=length)
    return [
        QueueSnapshot(phase_id=phase_id, queue_length=value, timestamp_s=float(idx))
        for idx, value in enumerate(queues)
    ]


def summarize_snapshots(snapshots: list[QueueSnapshot]) -> dict:
    analyzer = QueueDissipationAnalyzer()
    queues = [snap.queue_length for snap in snapshots]
    summary = analyzer.build_summary(queues)
    summary["count"] = len(snapshots)
    return summary


def group_by_phase(snapshots: list[QueueSnapshot]) -> dict:
    grouped: dict[str, list[int]] = {}
    for snap in snapshots:
        grouped.setdefault(snap.phase_id, []).append(snap.queue_length)
    return grouped


def interpolate_queues(queues: list[int], steps: int = 2) -> list[int]:
    if steps <= 1 or len(queues) < 2:
        return queues[:]
    interpolated = []
    for idx in range(len(queues) - 1):
        start = queues[idx]
        end = queues[idx + 1]
        for step in range(steps):
            fraction = step / steps
            value = int(round(start + (end - start) * fraction))
            interpolated.append(value)
    interpolated.append(queues[-1])
    return interpolated


def fake_phase_summary(phase_id: str, length: int = 8) -> dict:
    snapshots = fake_snapshots(phase_id=phase_id, length=length)
    return summarize_snapshots(snapshots)
