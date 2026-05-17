"""State reconciliation between simulation and orchestration layers."""
from dataclasses import dataclass
from typing import Dict

@dataclass
class StateSnapshot:
    vehicles: Dict[str, dict]
    signals: Dict[str, dict]
    timestamp_s: float

class StateReconciler:
    def reconcile(self, snapshot: StateSnapshot) -> StateSnapshot:
        return snapshot
