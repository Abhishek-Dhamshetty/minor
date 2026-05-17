"""Dynamic ETA estimator driven by live edge costs."""
from dataclasses import dataclass
from typing import Dict

@dataclass
class EtaSnapshot:
    edge_costs: Dict[str, float]
    timestamp_s: float

class DynamicEtaEstimator:
    def estimate(self, path_edges: list, snapshot: EtaSnapshot) -> float:
        return sum(snapshot.edge_costs.get(edge, 0.0) for edge in path_edges)
