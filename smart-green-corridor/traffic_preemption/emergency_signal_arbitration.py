"""Multi-intersection arbitration for competing emergency requests."""
from dataclasses import dataclass
from typing import List

@dataclass
class SignalRequest:
    tls_id: str
    vehicle_id: str
    priority: int
    distance_m: float

class EmergencySignalArbitration:
    def pick_winner(self, requests: List[SignalRequest]) -> SignalRequest | None:
        if not requests:
            return None
        return sorted(requests, key=lambda r: (-r.priority, r.distance_m))[0]
