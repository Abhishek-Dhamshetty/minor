"""Maintains live edge weights with smoothing and bounds."""
from dataclasses import dataclass
from typing import Dict

@dataclass
class WeightBounds:
    minimum: float
    maximum: float

class LiveEdgeWeightManager:
    def __init__(self, bounds: WeightBounds):
        self.bounds = bounds
        self.weights: Dict[str, float] = {}

    def update(self, edge_id: str, raw_cost: float) -> float:
        bounded = max(self.bounds.minimum, min(self.bounds.maximum, raw_cost))
        self.weights[edge_id] = bounded
        return bounded
