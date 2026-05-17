"""Analyzes congestion profiles across scenarios."""
from dataclasses import dataclass
from typing import Iterable


@dataclass
class CongestionEvent:
    corridor_id: str
    timestamp_s: float
    severity: float
    source: str


class CongestionAnalyzer:
    def score(self, timeline: list[float]) -> float:
        return sum(timeline) / max(1, len(timeline))

    def peak_index(self, timeline: list[float]) -> int:
        if not timeline:
            return -1
        max_value = max(timeline)
        return timeline.index(max_value)

    def normalize(self, timeline: list[float]) -> list[float]:
        if not timeline:
            return []
        max_value = max(timeline)
        if max_value <= 0:
            return [0.0 for _ in timeline]
        return [value / max_value for value in timeline]

    def bucketize(self, timeline: list[float], bucket_size: int) -> list[float]:
        if bucket_size <= 0:
            return []
        buckets = []
        for start in range(0, len(timeline), bucket_size):
            chunk = timeline[start : start + bucket_size]
            buckets.append(sum(chunk) / max(1, len(chunk)))
        return buckets

    def summarize(self, timeline: list[float]) -> dict:
        if not timeline:
            return {"min": 0.0, "max": 0.0, "avg": 0.0, "count": 0}
        return {
            "min": min(timeline),
            "max": max(timeline),
            "avg": self.score(timeline),
            "count": len(timeline),
        }

    def build_report(self, corridor_id: str, timeline: list[float]) -> dict:
        return {
            "corridor_id": corridor_id,
            "summary": self.summarize(timeline),
            "peak_index": self.peak_index(timeline),
            "normalized": self.normalize(timeline),
        }


def fake_load_timeline(length: int = 60, base: float = 0.4) -> list[float]:
    timeline = []
    for i in range(max(0, length)):
        wave = (i % 10) / 10.0
        timeline.append(base + wave)
    return timeline


def merge_timelines(timelines: Iterable[list[float]]) -> list[float]:
    merged = []
    for timeline in timelines:
        merged.extend(timeline)
    return merged


def event_stream_from_timeline(corridor_id: str, timeline: list[float]) -> list[CongestionEvent]:
    events: list[CongestionEvent] = []
    for idx, value in enumerate(timeline):
        events.append(
            CongestionEvent(
                corridor_id=corridor_id,
                timestamp_s=float(idx),
                severity=value,
                source="simulated",
            )
        )
    return events


def smooth_timeline(timeline: list[float], window: int = 3) -> list[float]:
    if window <= 1 or not timeline:
        return timeline[:]
    padded = [timeline[0]] * (window - 1) + timeline
    smoothed = []
    for idx in range(len(timeline)):
        segment = padded[idx : idx + window]
        smoothed.append(sum(segment) / len(segment))
    return smoothed


def fake_congestion_matrix(corridor_ids: list[str], length: int = 30) -> dict:
    return {corridor_id: fake_load_timeline(length=length) for corridor_id in corridor_ids}
