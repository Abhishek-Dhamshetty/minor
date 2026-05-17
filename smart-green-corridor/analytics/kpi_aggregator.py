"""Aggregates KPI metrics for dashboards."""
from dataclasses import dataclass
from typing import Dict

@dataclass
class KpiSnapshot:
    response_time_s: float
    travel_time_variance: float

class KpiAggregator:
    def aggregate(self, metrics: Dict[str, float]) -> KpiSnapshot:
        return KpiSnapshot(response_time_s=metrics.get("response_time_s", 0.0), travel_time_variance=metrics.get("travel_time_variance", 0.0))
