"""Mission planner for pickup and hospital drop-off phases."""
from dataclasses import dataclass
from typing import List

@dataclass
class MissionPhase:
    name: str
    target_edge: str

class MissionPlanner:
    def build_mission(self, pickup_edge: str, hospital_edge: str) -> List[MissionPhase]:
        return [MissionPhase(name="pickup", target_edge=pickup_edge), MissionPhase(name="dropoff", target_edge=hospital_edge)]
