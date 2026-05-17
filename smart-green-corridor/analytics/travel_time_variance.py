"""Computes travel time variance across missions."""
from dataclasses import dataclass


@dataclass
class TravelTimeSample:
    mission_id: str
    travel_time_s: float
    corridor_id: str


class TravelTimeVariance:
    def compute(self, samples: list[float]) -> float:
        if not samples:
            return 0.0
        mean = sum(samples) / len(samples)
        return sum((x - mean) ** 2 for x in samples) / len(samples)

    def stddev(self, samples: list[float]) -> float:
        variance = self.compute(samples)
        return variance ** 0.5

    def coefficient_of_variation(self, samples: list[float]) -> float:
        if not samples:
            return 0.0
        mean = sum(samples) / len(samples)
        if mean <= 0:
            return 0.0
        return self.stddev(samples) / mean

    def summarize(self, samples: list[float]) -> dict:
        return {
            "variance": self.compute(samples),
            "stddev": self.stddev(samples),
            "cv": self.coefficient_of_variation(samples),
        }


def fake_samples(count: int = 6, base: float = 320.0) -> list[TravelTimeSample]:
    samples: list[TravelTimeSample] = []
    for idx in range(max(0, count)):
        samples.append(
            TravelTimeSample(
                mission_id=f"M-{2000 + idx}",
                travel_time_s=base + (idx % 4) * 12.5,
                corridor_id=f"C-{idx % 3}",
            )
        )
    return samples


def summarize_samples(samples: list[TravelTimeSample]) -> dict:
    variance = TravelTimeVariance()
    values = [sample.travel_time_s for sample in samples]
    summary = variance.summarize(values)
    summary["count"] = len(samples)
    return summary


def group_by_corridor(samples: list[TravelTimeSample]) -> dict:
    grouped: dict[str, list[float]] = {}
    for sample in samples:
        grouped.setdefault(sample.corridor_id, []).append(sample.travel_time_s)
    return grouped


def build_corridor_variances(samples: list[TravelTimeSample]) -> dict:
    variance = TravelTimeVariance()
    grouped = group_by_corridor(samples)
    return {corridor_id: variance.compute(values) for corridor_id, values in grouped.items()}


def percentile(samples: list[float], pct: float) -> float:
    if not samples:
        return 0.0
    ordered = sorted(samples)
    index = int(round((pct / 100.0) * (len(ordered) - 1)))
    return ordered[max(0, min(len(ordered) - 1, index))]


def fake_histogram(samples: list[float], bucket: float = 20.0) -> dict:
    histogram: dict[str, int] = {}
    for value in samples:
        start = int(value // bucket) * bucket
        end = start + bucket
        label = f"{start:.0f}-{end:.0f}"
        histogram[label] = histogram.get(label, 0) + 1
    return histogram
