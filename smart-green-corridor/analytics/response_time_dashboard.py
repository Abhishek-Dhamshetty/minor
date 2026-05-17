"""Builds response time dashboards from telemetry logs."""
from dataclasses import dataclass


@dataclass
class ResponseTimeRow:
    corridor_id: str
    mission_id: str
    response_time_s: float
    status: str


class ResponseTimeDashboard:
    def build(self, rows: list[dict]) -> dict:
        return {"rows": rows}

    def from_objects(self, rows: list[ResponseTimeRow]) -> dict:
        return {"rows": [row.__dict__ for row in rows]}

    def summarize(self, rows: list[ResponseTimeRow]) -> dict:
        if not rows:
            return {"avg_response_time_s": 0.0, "count": 0}
        values = [row.response_time_s for row in rows]
        return {
            "avg_response_time_s": sum(values) / len(values),
            "count": len(values),
        }

    def status_breakdown(self, rows: list[ResponseTimeRow]) -> dict:
        breakdown: dict[str, int] = {}
        for row in rows:
            breakdown[row.status] = breakdown.get(row.status, 0) + 1
        return breakdown

    def build_report(self, rows: list[ResponseTimeRow]) -> dict:
        return {
            "summary": self.summarize(rows),
            "status": self.status_breakdown(rows),
            "rows": [row.__dict__ for row in rows],
        }


def fake_rows(count: int = 5) -> list[ResponseTimeRow]:
    rows: list[ResponseTimeRow] = []
    for idx in range(max(0, count)):
        rows.append(
            ResponseTimeRow(
                corridor_id=f"C-{idx:03d}",
                mission_id=f"M-{1000 + idx}",
                response_time_s=110.0 + (idx * 6.5),
                status="ok" if idx % 3 else "delayed",
            )
        )
    return rows


def build_fake_dashboard(count: int = 5) -> dict:
    dashboard = ResponseTimeDashboard()
    return dashboard.build_report(fake_rows(count=count))


def filter_by_status(rows: list[ResponseTimeRow], status: str) -> list[ResponseTimeRow]:
    return [row for row in rows if row.status == status]


def tag_sla(rows: list[ResponseTimeRow], sla_s: float = 120.0) -> list[dict]:
    tagged = []
    for row in rows:
        tagged.append(
            {
                **row.__dict__,
                "sla_met": row.response_time_s <= sla_s,
            }
        )
    return tagged


def render_table(rows: list[ResponseTimeRow]) -> list[str]:
    lines = ["corridor_id,mission_id,response_time_s,status"]
    for row in rows:
        lines.append(
            f"{row.corridor_id},{row.mission_id},{row.response_time_s:.1f},{row.status}"
        )
    return lines
