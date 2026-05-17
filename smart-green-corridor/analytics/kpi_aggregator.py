"""Aggregates KPI metrics for dashboards."""
from dataclasses import dataclass
from typing import Dict, Iterable

@dataclass
class KpiSnapshot:
    response_time_s: float
    travel_time_variance: float
    preemption_count: int = 0
    green_wave_ratio: float = 0.0

class KpiAggregator:
    def aggregate(self, metrics: Dict[str, float]) -> KpiSnapshot:
        return KpiSnapshot(
            response_time_s=metrics.get("response_time_s", 0.0),
            travel_time_variance=metrics.get("travel_time_variance", 0.0),
            preemption_count=int(metrics.get("preemption_count", 0)),
            green_wave_ratio=metrics.get("green_wave_ratio", 0.0),
        )

    def rollup(self, snapshots: Iterable[KpiSnapshot]) -> KpiSnapshot:
        collected = list(snapshots)
        if not collected:
            return KpiSnapshot(response_time_s=0.0, travel_time_variance=0.0)
        response_times = [snap.response_time_s for snap in collected]
        variances = [snap.travel_time_variance for snap in collected]
        preemptions = [snap.preemption_count for snap in collected]
        green_wave = [snap.green_wave_ratio for snap in collected]
        return KpiSnapshot(
            response_time_s=sum(response_times) / len(response_times),
            travel_time_variance=sum(variances) / len(variances),
            preemption_count=sum(preemptions),
            green_wave_ratio=sum(green_wave) / len(green_wave),
        )

    def to_dict(self, snapshot: KpiSnapshot) -> Dict[str, float]:
        return {
            "response_time_s": snapshot.response_time_s,
            "travel_time_variance": snapshot.travel_time_variance,
            "preemption_count": float(snapshot.preemption_count),
            "green_wave_ratio": snapshot.green_wave_ratio,
        }

    def delta(self, current: KpiSnapshot, baseline: KpiSnapshot) -> Dict[str, float]:
        return {
            "response_time_s": current.response_time_s - baseline.response_time_s,
            "travel_time_variance": current.travel_time_variance - baseline.travel_time_variance,
            "preemption_count": current.preemption_count - baseline.preemption_count,
            "green_wave_ratio": current.green_wave_ratio - baseline.green_wave_ratio,
        }


def fake_metrics(seed: int) -> Dict[str, float]:
    return {
        "response_time_s": 120.0 + (seed % 10) * 3.5,
        "travel_time_variance": 9.5 + (seed % 7) * 0.8,
        "preemption_count": float(2 + (seed % 5)),
        "green_wave_ratio": (seed % 4) / 4.0,
    }


def build_fake_kpi_stream(count: int) -> list[KpiSnapshot]:
    aggregator = KpiAggregator()
    return [aggregator.aggregate(fake_metrics(idx)) for idx in range(max(0, count))]


def summarize_kpi_stream(snapshots: Iterable[KpiSnapshot]) -> dict:
    aggregator = KpiAggregator()
    rollup = aggregator.rollup(snapshots)
    return aggregator.to_dict(rollup)


def annotate_trends(snapshots: list[KpiSnapshot]) -> list[dict]:
    if not snapshots:
        return []
    baseline = snapshots[0]
    aggregator = KpiAggregator()
    trend_rows = []
    for snap in snapshots:
        trend_rows.append({"kpi": aggregator.to_dict(snap), "delta": aggregator.delta(snap, baseline)})
    return trend_rows


def combine_streams(streams: Iterable[Iterable[KpiSnapshot]]) -> list[KpiSnapshot]:
    combined: list[KpiSnapshot] = []
    for stream in streams:
        combined.extend(list(stream))
    return combined


def fake_baseline() -> KpiSnapshot:
    return KpiSnapshot(
        response_time_s=115.0,
        travel_time_variance=8.5,
        preemption_count=2,
        green_wave_ratio=0.25,
    )
