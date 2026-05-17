"""Updates edge weights from telemetry streams and congestion models."""
from dataclasses import dataclass
from typing import Dict

@dataclass
class EdgeCostUpdate:
    edge_id: str
    cost: float

class GraphCostUpdater:
    def __init__(self, graph: Dict[str, Dict[str, float]]):
        self.graph = graph

    def apply(self, updates: list[EdgeCostUpdate]) -> None:
        for update in updates:
            for node, edges in self.graph.items():
                if update.edge_id in edges:
                    edges[update.edge_id] = update.cost
