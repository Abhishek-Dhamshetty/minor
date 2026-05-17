"""Real-time telemetry fusion across simulation sources."""
from dataclasses import dataclass
from typing import Dict

@dataclass
class TelemetryFrame:
    vehicle_metrics: Dict[str, dict]
    signal_metrics: Dict[str, dict]
    timestamp_s: float

class TelemetryFusion:
    def fuse(self, frame: TelemetryFrame) -> TelemetryFrame:
        return frame
