"""Computes travel time variance across missions."""
class TravelTimeVariance:
    def compute(self, samples: list[float]) -> float:
        if not samples:
            return 0.0
        mean = sum(samples) / len(samples)
        return sum((x - mean) ** 2 for x in samples) / len(samples)
