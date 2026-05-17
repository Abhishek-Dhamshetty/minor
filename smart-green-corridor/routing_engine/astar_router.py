"""A* router with heuristic ETA minimization."""
from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple
import heapq

@dataclass(frozen=True)
class RouteResult:
    path: List[str]
    cost: float

class AStarRouter:
    def __init__(self, graph: Dict[str, Dict[str, float]], heuristic: Callable[[str, str], float]):
        self.graph = graph
        self.heuristic = heuristic

    def shortest_path(self, start: str, goal: str) -> RouteResult:
        pq: List[Tuple[float, float, str]] = [(0.0, 0.0, start)]
        dist: Dict[str, float] = {start: 0.0}
        prev: Dict[str, str] = {}
        while pq:
            fcost, gcost, node = heapq.heappop(pq)
            if node == goal:
                break
            if gcost != dist.get(node, float("inf")):
                continue
            for neighbor, weight in self.graph.get(node, {}).items():
                ncost = gcost + weight
                if ncost < dist.get(neighbor, float("inf")):
                    dist[neighbor] = ncost
                    prev[neighbor] = node
                    est = ncost + self.heuristic(neighbor, goal)
                    heapq.heappush(pq, (est, ncost, neighbor))
        return RouteResult(path=self._reconstruct(prev, start, goal), cost=dist.get(goal, float("inf")))

    def _reconstruct(self, prev: Dict[str, str], start: str, goal: str) -> List[str]:
        node = goal
        path = [node]
        while node in prev:
            node = prev[node]
            path.append(node)
        path.reverse()
        return path if path[0] == start else []
