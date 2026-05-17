"""Emergency dispatch orchestrator with nearest-ambulance selection."""
from dataclasses import dataclass
from typing import Dict, Tuple

@dataclass
class EmergencyRequest:
    request_id: str
    location: Tuple[float, float]
    priority: int

class EmergencyDispatcher:
    def __init__(self, fleet_index: Dict[str, Tuple[float, float]]):
        self.fleet_index = fleet_index

    def select_nearest(self, request: EmergencyRequest) -> str:
        best_id = ""
        best_dist = float("inf")
        for amb_id, coords in self.fleet_index.items():
            dist = (coords[0] - request.location[0]) ** 2 + (coords[1] - request.location[1]) ** 2
            if dist < best_dist:
                best_dist = dist
                best_id = amb_id
        return best_id
