# Emergency Traffic Preemption (Web UI)

This repository contains a software-only web simulation of an emergency traffic preemption system for Hyderabad. It visualizes ambulances, hospitals, traffic signals, preemption behavior, and dispatch notifications.

## What this includes

- Interactive map simulation with ambulance dispatch, signal preemption, and traffic behavior.
- Notifications page for dispatch updates and live ambulance follow links.
- Analytics dashboard showing dispatch metrics and charts.
- Static data files used by the UI.

## Quick start

From the repository root:

```bash
python3 -m http.server 8000
```

Open the web UI:

```text
http://localhost:8000/web/index.html
```

Notifications and analytics:

```text
http://localhost:8000/web/notifications.html
http://localhost:8000/web/analytics.html
```

## Project layout

- `web/index.html`: main simulation UI
- `web/notifications.html`: dispatch notifications
- `web/analytics.html`: analytics dashboard
- `hyderabad_hospitals.csv`: hospital locations used by the UI
- `hyderabad.net.xml`: traffic lights used by the UI

## Notes

- This is a software-only simulation (no hardware integration).
- The map uses OpenStreetMap tiles and OSRM routing (public endpoints).
- The notifications and analytics pages use localStorage for data sharing in the browser.
  python smart_emergency_system.py --sumocfg hyderabad.sumocfg --sumo-binary sumo

````

## 5.2) Phase-1 Real-World Data + Police Alerts

The controller now supports realtime roadside ingestion, LoRa map-matching, merged routing costs in `dijkstra/astar`, and police notifications.

### New runtime options

```powershell
python smart_emergency_system.py `
  --sumocfg hyderabad.sumocfg `
  --routing-algorithm dijkstra `
  --live-traffic-file out/live_traffic.json `
  --lora-events-file out/lora_events.jsonl `
  --police-log out/police_notifications.jsonl `
  --write-web-state
````

### Live feed inputs

Provide live-feed files directly:

1. `out/live_traffic.json`
2. `out/lora_events.jsonl`

Optional API endpoint for traffic police command center:

```powershell
python smart_emergency_system.py --sumocfg hyderabad.sumocfg --police-endpoint http://127.0.0.1:9000/police/alerts
```

### `out/live_traffic.json` format

```json
{
  "timestamp": 1710000000,
  "edges": [
    {
      "edge_id": "25286049#0",
      "speed_kmh": 14.0,
      "occupancy": 0.72,
      "confidence": 0.9,
      "incident": false
    }
  ]
}
```

### `out/lora_events.jsonl` format

Each line is one JSON object:

```json
{
  "timestamp": 1710000000,
  "ambulance_id": "ambulance_1",
  "lat": 17.4401,
  "lon": 78.3902,
  "emergency": true
}
```

### Dashboard fields added

Web dashboard now shows:

1. Trigger confidence
2. Selected corridor TLS IDs
3. Reroute reason (per ambulance)
4. Police notification status

### Signal behavior update

1. Runner no longer forces always-on green corridor.
2. Emergency preemption now uses realistic transition windows:

- yellow transition (`yellow_transition_s`, default 3s)
- all-red clearance (`all_red_s`, default 2s)

3. Green hold duration is demand-adaptive and bounded (`min_dynamic_green_s`..`max_dynamic_green_s`, default 18..70s).
4. Anti-oscillation guards reduce rapid TLS flipping:

- minimum owner hold (`min_owner_hold_s`)
- post-restore cooldown (`post_restore_cooldown_s`)

5. After preemption release, TLS returns to baseline SUMO program.

## 5.4) User Web Call -> Ambulance Dispatch -> Hospital Reroute

1. User clicks location on dashboard map and raises emergency call (`/api/call`).
2. Call is appended to `out/call_requests.jsonl`.
3. Controller map-matches call location and assigns nearest idle ambulance.
4. Ambulance first routes to caller edge (`dispatch_to_caller`).
5. After pickup, reroutes to best hospital using live merged traffic costs.
6. Green-corridor and police notifications continue for that mission.

Health-only constraint:

- `emergency_type` must be one of `trauma`, `cardiac`, `stroke`, or `general`.
- Non-health request types (for example fire/disaster) are rejected by the API for this ambulance corridor pipeline.

Call API now supports preferred hospital hint:

```json
{
  "caller_name": "citizen",
  "emergency_type": "trauma",
  "lat": 17.4412,
  "lon": 78.3921,
  "preferred_hospital_id": "image_hospitals"
}
```

If preferred hospital ETA is within configured tolerance (`--preferred-hospital-max-extra-eta-s`), it is selected.

## 5.6) Police Mobile SMS Notifications

You can send police alerts directly to a mobile number (not only dashboard logs).

Required environment variables:

```powershell
$env:TWILIO_ACCOUNT_SID = "<sid>"
$env:TWILIO_AUTH_TOKEN = "<token>"
$env:TWILIO_FROM_NUMBER = "+1XXXXXXXXXX"
```

Run with police mobile target:

```powershell
.\run_hyderabad.ps1 -StartWebDashboard -PoliceMobile "+91XXXXXXXXXX"
```

## 5.7) React Web UI

`web/index.html` is now a React-based single-page UI (CDN React + component state + Leaflet map) with:

1. realtime feed health
2. map-based call dispatch
3. preferred hospital selection
4. fleet/call timeline panels

The dashboard also includes:

1. persistent auth-backed login for user and traffic police roles
2. user self-registration (`/api/auth/register` for role `user`)
3. token profile endpoint (`/api/auth/profile`)

## 5.5) Ambulances Initially Stationed At Hospitals

Runner now generates emergency fleet from hospitals (3 ambulances per hospital edge):

```powershell
python create_stationed_ambulance_routes.py --config config/hyderabad_example.json --net hyderabad.net.xml --out emergency_vehicle.rou.xml --per-hospital 3
```

`run_hyderabad.ps1` uses this generation path by default.

## 5.1) Parallel Realtime Web Dashboard

SUMO workflow remains unchanged; you can run a parallel web map using exported realtime state.

1. Start simulation as usual:

```powershell
.\run_hyderabad.ps1
```

2. In a second terminal, launch dashboard server:

```powershell
python web/realtime_server.py --host 127.0.0.1 --port 8090
```

3. Open:

```text
http://127.0.0.1:8090
```

## 6) Hyderabad hospital customization

Edit `hyderabad_hospitals.csv` with:

- Current capacity values
- Specialization flags (`supports_trauma`, `supports_cardiac`, `supports_stroke`)
- Local HTTP endpoint for each hospital if available

If endpoint is blank/offline, notifications are stored in:

- `out/hospital_notifications.jsonl`

## 7) How rerouting works

For each verification event, the system:

1. Calculates ETA from ambulance current edge to each hospital entry edge using SUMO route finding.
2. Filters hospitals by emergency type and available capacity.
3. Chooses best score (ETA with capacity preference).
4. Applies route update via TraCI.
5. Pre-notifies destination hospital.

Implementation location for rerouting:

1. `route_planner.py` contains ETA estimation and route construction.
2. `smart_emergency_system.py` invokes rerouting every configured interval (`--reroute-interval-s` / profile override).
3. You can select shortest-path engine: `--routing-algorithm sumo|dijkstra|astar`.
4. For `dijkstra` and `astar`, route cost uses live SUMO edge travel times (congestion-aware) with static fallback.

Implementation location for dedicated emergency priority:

1. `emergency_vehicle.rou.xml` and `create_multi_ambulance_routes.py` define `vClass="emergency"` and blue-light/siren parameters.
2. `signal_preemption.py` enforces multi-intersection green-corridor preemption.
3. `smart_emergency_system.py` applies runtime emergency parameters and preemption ownership fairness.

Current limitation:

1. Physical dedicated ambulance-only lanes depend on lane permissions in `hyderabad.net.xml`.
2. This project currently prioritizes ambulances through dynamic rerouting + signal preemption, not static lane redesign.

## 7.1) Multi-ambulance priority conflict handling

When two ambulances request conflicting movements at one traffic signal:

1. Controller scores incoming requests by priority and approach distance.
2. It grants ownership of the signal to one ambulance for a bounded hold window.
3. It prevents rapid oscillation via minimum switch interval.
4. It rebalances and hands over to the next ambulance after fairness window expires.

## 7.2) GUI visualization

When you run with `-SumoBinary sumo-gui`, the simulation shows:

1. Hospital markers as red plus symbols from `hospital_markers.add.xml`.
2. Emergency vehicles in bright dedicated colors.
3. Signal preemption logs in terminal (`[SIGNAL] ...`) showing phase changes and restoration.
4. Mixed traffic with cars, bikes, and pedestrians.

## 8) Green Corridor Tracking (Detailed)

This project tracks and enforces green corridor behavior through these runtime stages:

1. Emergency vehicle detection:
   `smart_emergency_system.py` identifies active ambulances by type/id.
2. Junction scan:
   For each ambulance, `traci.vehicle.getNextTLS` is used to find upcoming signals.
3. Priority scoring:
   Closer ambulances with higher emergency priority get stronger score.
4. Signal control:
   `signal_preemption.py` sets the desired phase to green for the winning ambulance movement.
5. Ownership fairness:
   Ownership windows avoid rapid oscillation between ambulances.
6. Restore logic:
   Signals are restored to baseline after corridor window ends.

Telemetry keys:

1. `[SIGNAL] ...` lines show preemption and restore actions.
2. `[ASSERT] ... active_tls_preempted=` gives active preempted signal count.
3. Web dashboard `signals` layer shows red/yellow-or-orange/green with preempted flag.

## 9) Realtime Dashboard (Project Ops)

Preferred run command (single command):

```powershell
.\run_hyderabad.ps1 -StartWebDashboard
```

If started manually, use workspace-relative path:

```powershell
python web/realtime_server.py --host 127.0.0.1 --port 8090
```

Open browser:

```text
http://127.0.0.1:8090
```

Dashboard capabilities:

1. Ambulance status: `enroute | reached | breakdown`.
2. Arrival timeline with elapsed dispatch-to-hospital times.
3. Signal markers with current color and preemption status.
4. Layer switcher including satellite basemap for flyover inspection.
5. Popup notifications for reached/breakdown transitions.

## 10) Route and Hospital Assignment Policy

To avoid fleet pile-up at one hospital:

1. Hospital ETA is adjusted with load penalty (`hospital_load_by_id`).
2. Assigned hospital is kept stable per ambulance to avoid oscillation.
3. Stop positions are lane/position staggered per hospital (`hospital_stop_slots`).
4. Hospital load is released when ambulance reaches or breaks down.

## 11) Event Semantics

1. `ARRIVAL`:
   Logged once when ambulance is on destination hospital edge and nearly stopped.
2. `BREAKDOWN`:
   Logged when vehicle remains stopped beyond configured threshold on non-internal edge.
3. `SUMMARY`:
   Logged when all ambulances are completed (reached + breakdown).

## 12) Recommended Validation Checklist

1. Confirm at least one signal preemption in `[SIGNAL]` logs.
2. Confirm dashboard shows non-zero `active_tls_preempted` during emergency windows.
3. Confirm arrivals populate timeline with elapsed seconds.
4. Confirm no repeated arrival line for same ambulance.
5. Confirm hospitals are load-distributed across fleet under congestion.
6. Ambulance debug camera mode: auto-tracks and highlights active ambulances in SUMO GUI.

You can tune camera behavior with controller options:

1. `--ambulance-debug-gui`
2. `--camera-switch-interval-s 5.0`
3. `--camera-zoom 1700`

## 7.3) LoRa integration (UDP gateway)

If your LoRa gateway forwards packets over UDP, run:

```powershell
python smart_emergency_system.py --sumocfg hyderabad.sumocfg --sumo-binary sumo-gui --auto-detect-emergency-vehicles --lora-udp-host 127.0.0.1 --lora-udp-port 1700
```

Any UDP payload received on that socket is treated as a wireless trigger.

Runner passthrough parameters:

```powershell
.\run_hyderabad.ps1 -Profile strict-production -SumoBinary sumo-gui -LoraUdpHost 127.0.0.1 -LoraUdpPort 1700
```

## 10) Project objectives presentation

Generate an objectives deck:

```powershell
python create_project_objectives_ppt.py
```

Output file:

- `Project_Objectives_Emergency_Traffic.pptx`

## 8) Scaling to city grid

For wider smart-city scaling:

1. Partition the city into control zones.
2. Run one edge controller per zone.
3. Use corridor handoff by forwarding vehicle ID + route corridor to adjacent zone controller.
4. Keep local fallback logic if inter-zone communication drops.

## 9) Quick validation checklist

1. Dual verification must be true before preemption occurs.
2. Corridor preemption should affect multiple upcoming intersections.
3. Route should change when traffic/ETA changes.
4. Hospital notification should appear in endpoint or local JSONL log.
5. Traffic lights should return to baseline after ambulance passes.
