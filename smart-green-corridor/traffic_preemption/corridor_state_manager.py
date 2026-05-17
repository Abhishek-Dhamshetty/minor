"""Corridor ownership and preemption state manager."""
from dataclasses import dataclass
from typing import Dict

@dataclass
class CorridorState:
    owner_vehicle: str
    expires_at_s: float

class CorridorStateManager:
    def __init__(self) -> None:
        self.active: Dict[str, CorridorState] = {}

    def assign(self, tls_id: str, state: CorridorState) -> None:
        self.active[tls_id] = state

    def release(self, tls_id: str) -> None:
        self.active.pop(tls_id, None)
