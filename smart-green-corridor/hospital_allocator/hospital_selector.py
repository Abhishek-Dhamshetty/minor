"""Hospital selection with capacity-aware scoring."""
from dataclasses import dataclass
from typing import List

@dataclass
class Hospital:
    hospital_id: str
    edge_id: str
    capacity: int

class HospitalSelector:
    def pick(self, hospitals: List[Hospital]) -> Hospital | None:
        if not hospitals:
            return None
        return sorted(hospitals, key=lambda h: (-h.capacity, h.hospital_id))[0]
