"""Dijkstra-based router with congestion-aware weights."""
from dataclasses import dataclass
from typing import Dict, List, Tuple
import heapq

@dataclass(frozen=True)
class RouteResult:
    path: List[str]
    cost: float

class DijkstraRouter:
    def __init__(self, graph: Dict[str, Dict[str, float]]):
        self.graph = graph

    def shortest_path(self, start: str, goal: str) -> RouteResult:
        pq: List[Tuple[float, str]] = [(0.0, start)]
        dist: Dict[str, float] = {start: 0.0}
        prev: Dict[str, str] = {}
        while pq:
            cost, node = heapq.heappop(pq)
            if node == goal:
                break
            if cost != dist.get(node, float("inf")):
                continue
            for neighbor, weight in self.graph.get(node, {}).items():
                ncost = cost + weight
                if ncost < dist.get(neighbor, float("inf")):
                    dist[neighbor] = ncost
                    prev[neighbor] = node
                    heapq.heappush(pq, (ncost, neighbor))
        return RouteResult(path=self._reconstruct(prev, start, goal), cost=dist.get(goal, float("inf")))

    def _reconstruct(self, prev: Dict[str, str], start: str, goal: str) -> List[str]:
        node = goal
        path = [node]
        while node in prev:
            node = prev[node]
            path.append(node)
        path.reverse()
        return path if path[0] == start else []
