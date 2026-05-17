"""Measures corridor efficiency and preemption impact."""
from dataclasses import dataclass


@dataclass
class EfficiencySample:
    corridor_id: str
    preemptions: int
    clearance_s: float
    green_wave_hits: int


class CorridorEfficiencyMetrics:
    def compute(self, preemptions: int, clearance_s: float) -> float:
        return preemptions / max(1.0, clearance_s)

    def green_wave_ratio(self, hits: int, attempts: int) -> float:
        if attempts <= 0:
            return 0.0
        return hits / attempts

    def clearance_penalty(self, clearance_s: float, target_s: float = 90.0) -> float:
        if clearance_s <= 0:
            return 1.0
        return min(2.0, clearance_s / target_s)

    def composite_score(self, sample: EfficiencySample) -> float:
        base = self.compute(sample.preemptions, sample.clearance_s)
        wave = self.green_wave_ratio(sample.green_wave_hits, sample.preemptions)
        penalty = self.clearance_penalty(sample.clearance_s)
        return (base + wave) / penalty

    def summarize_samples(self, samples: list[EfficiencySample]) -> dict:
        if not samples:
            return {"avg_score": 0.0, "count": 0}
        scores = [self.composite_score(sample) for sample in samples]
        return {"avg_score": sum(scores) / len(scores), "count": len(samples)}


def fake_samples(corridor_ids: list[str]) -> list[EfficiencySample]:
    samples: list[EfficiencySample] = []
    for idx, corridor_id in enumerate(corridor_ids):
        samples.append(
            EfficiencySample(
                corridor_id=corridor_id,
                preemptions=1 + (idx % 5),
                clearance_s=60.0 + (idx * 4.5),
                green_wave_hits=idx % 3,
            )
        )
    return samples


def build_efficiency_report(samples: list[EfficiencySample]) -> dict:
    metrics = CorridorEfficiencyMetrics()
    summary = metrics.summarize_samples(samples)
    return {
        "summary": summary,
        "samples": [sample.__dict__ for sample in samples],
    }


def mock_corridor_ranking(samples: list[EfficiencySample]) -> list[tuple[str, float]]:
    metrics = CorridorEfficiencyMetrics()
    ranked = [(sample.corridor_id, metrics.composite_score(sample)) for sample in samples]
    ranked.sort(key=lambda item: item[1], reverse=True)
    return ranked


def fake_benchmark(sample: EfficiencySample) -> dict:
    metrics = CorridorEfficiencyMetrics()
    return {
        "corridor_id": sample.corridor_id,
        "score": metrics.composite_score(sample),
        "target": 0.5,
        "status": "ok" if metrics.composite_score(sample) >= 0.5 else "needs_tuning",
    }


def clamp_score(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


def apply_weighting(score: float, weight: float = 1.0) -> float:
    return clamp_score(score * weight)


def build_fake_series(samples: list[EfficiencySample]) -> list[dict]:
    metrics = CorridorEfficiencyMetrics()
    series = []
    for sample in samples:
        series.append(
            {
                "corridor_id": sample.corridor_id,
                "score": metrics.composite_score(sample),
                "weighted": apply_weighting(metrics.composite_score(sample), 0.9),
            }
        )
    return series
