# Smart Emergency Vehicle Preemption System for Green Corridor Traffic Management

A research-grade, simulation-only emergency traffic orchestration framework built on SUMO and TraCI.
This repository is a large-scale academic scaffold designed to demonstrate advanced routing, signal
preemption, congestion prediction, and multi-agent coordination for emergency response.

## Architecture Overview

- SUMO-based city-scale simulation with OpenStreetMap-derived networks.
- TraCI orchestration layer for real-time control and telemetry capture.
- Multi-algorithm routing engine (Dijkstra, A*, Bidirectional A*).
- Queue-aware signal preemption with corridor ownership scheduling.
- Streaming telemetry over WebSocket, Kafka, and MQTT with Redis caching.
- AI/ML modules for congestion prediction and signal optimization (simulation-only).
- Observability stack with Prometheus and Grafana dashboards.

## End-to-End Workflow

1. Operator clicks a map location to generate an emergency request.
2. Dispatch core selects nearest ambulance and computes an optimal route.
3. Signal control creates a green corridor and arbitrates multi-intersection ownership.
4. Routing engine performs congestion-aware re-planning in real time.
5. Ambulance executes pickup and hospital drop-off mission.
6. Signal phases restore to baseline after clearance.

## Algorithms Implemented

Routing:

- Dijkstra, A*, Bidirectional A*
- Dynamic edge weighting with congestion-aware rerouting
- Heuristic ETA minimization with fallback strategies

Signal Control:

- Queue-pressure adaptive green extension
- Rolling horizon optimization
- Max-pressure traffic control
- Emergency signal arbitration
- Green-wave synchronization
- Corridor ownership scheduling

AI/ML:

- LSTM congestion prediction (simulation-only)
- Reinforcement learning signal agent (simulation-only)
- Graph neural network traffic estimation (simulation-only)
- Temporal demand forecasting (simulation-only)

## Deployment Architecture

- SUMO containers for simulation runs
- FastAPI gateway for dispatch APIs
- WebSocket streaming for live telemetry
- Redis + Kafka + RabbitMQ for event and task flows
- Postgres/PostGIS for storage and geospatial indexing
- Prometheus + Grafana for metrics and dashboards

## Simulation Pipeline

- Network import from OSM and SUMO net conversion
- Route generation, traffic demand synthesis, and scenario configs
- Real-time orchestration via TraCI
- Telemetry ingestion and analytics
- Deterministic seed manager for reproducibility

## KPI Metrics

- Response time and travel time variance
- Queue dissipation and corridor efficiency
- Signal phase preemption frequency
- Congestion resilience under stress scenarios

## Benchmarking

- Scenario runners for peak-hour and multi-ambulance stress tests
- Ablation studies for routing and signal policies
- Reproducible experiment registry

## Scalability Notes

- Event-driven architecture for high-frequency state updates
- Distributed coordination for multi-agent arbitration
- Horizontal scaling for telemetry and analytics workloads

## Future Scope

- Hardware-in-the-loop validation
- Extended RL agents for adaptive signal control
- Dynamic demand shaping under city-wide constraints

## Disclaimer

This repository is a simulation-only academic scaffold. It does not claim any physical deployment
or real-world emergency vehicle integration.
