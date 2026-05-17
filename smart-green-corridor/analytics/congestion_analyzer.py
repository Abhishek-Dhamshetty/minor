"""Analyzes congestion profiles across scenarios."""
class CongestionAnalyzer:
    def score(self, timeline: list[float]) -> float:
        return sum(timeline) / max(1, len(timeline))
