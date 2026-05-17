"""Selects a routing strategy based on congestion regime."""
from dataclasses import dataclass
from typing import Protocol

class Router(Protocol):
    def shortest_path(self, start: str, goal: str):
        ...

@dataclass
class HybridPathSelector:
    dijkstra: Router
    astar: Router

    def choose(self, congestion_index: float) -> Router:
        return self.astar if congestion_index > 0.6 else self.dijkstra
