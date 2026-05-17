"""Builds response time dashboards from telemetry logs."""
class ResponseTimeDashboard:
    def build(self, rows: list[dict]) -> dict:
        return {"rows": rows}
