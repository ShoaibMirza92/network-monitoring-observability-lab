# Network Monitoring & Observability Lab

A simulated Network Monitoring & Observability Lab for portfolio and training purposes. This repository implements a small, self-contained Python monitoring simulation that demonstrates device availability checks, simulated ICMP/latency, CPU/memory metrics, interface status, packet-loss detection, threshold-based alerting, reporting, and unit testing — all using simulated data. No real network devices, credentials, or production information are used.

Repository contents
- config/
  - devices.json — simulated device inventory (RFC1918/private IPs)
  - thresholds.json — monitoring thresholds and small probabilities used by the simulator
- src/
  - monitor.py — orchestrator and deterministic simulator (seeded RNG)
  - alerts.py — threshold evaluation and alert generation
  - reporting.py — console report and CSV writer
- tests/
  - test_monitor.py — pytest unit tests covering inventory, deterministic simulation, alerting, and report writing
- docs/
  - architecture.md — architecture description
  - troubleshooting.md — realistic troubleshooting scenarios
- diagrams/
  - network-topology.md — Mermaid network topology
- requirements.txt — minimal dependency (pytest)

Quick start (Windows PowerShell)
1. Clone the repository
   git clone https://github.com/ShoaibMirza92/network-monitoring-observability-lab.git
   cd network-monitoring-observability-lab

2. Create and activate a Python virtual environment
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   # If PowerShell blocks activation, run (once) as admin:
   # Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

3. Install dependencies
   pip install -r requirements.txt

4. Run the monitoring simulation
   python -m src.monitor

   What this does:
   - Loads config/devices.json and config/thresholds.json
   - Simulates availability, CPU, memory, interfaces, packet loss, and latency for each device using a seeded RNG
   - Evaluates alerts using src/alerts.py against thresholds
   - Prints a console report and writes a CSV report `report_network_monitoring.csv` in the current working directory

5. Run the tests
   pytest -q

Implementation notes
- Deterministic simulation: `src.monitor.run_monitor(seed=...)` uses a seeded random generator so tests can reproduce the same simulated output.
- Separation of concerns: monitoring simulation (src/monitor.py), alert evaluation (src/alerts.py), and reporting (src/reporting.py) are separate modules for clarity and testability.
- No external network I/O: the code intentionally simulates ICMP, SNMP, and syslog behavior — it does not perform real pings or SNMP queries.

Sample CLI output (example)
```
============================================================
Network Monitoring Report (simulated)
Timestamp: 2026-09-06T00:00:00.000000
Total devices: 6
Healthy devices (no critical alerts): 5
Warning alerts: 1
Critical alerts: 0
------------------------------------------------------------
CORE-RTR-01          UP     CPU: 23.4 MEM: 29.8 LAT: 12ms PL: 0.12%
CORE-SW-01           UP     CPU: 8.7  MEM: 18.3 LAT: 5ms  PL: 0.05%
... (other devices)
------------------------------------------------------------
Alerts:
[WARNING] CORE-RTR-01 - cpu = 78.2 (thr: 75.0) -> Monitor CPU usage; check routes and recent changes
============================================================
CSV report written to: report_network_monitoring.csv
```

What to do if something fails
- If a config file is missing, the application prints an explicit error referencing the missing file path.
- If pytest fails, inspect the failing test and run the monitor with a fixed seed to reproduce the issue.

Extending the lab
- Add a mock SNMP agent or simulated time-series DB (InfluxDB) for richer visualization — keep it simulated to avoid any production connections.
- Add a small Grafana dashboard (JSON) for demonstration (static mock values).

Disclaimer
This is a simulated lab for learning and demonstration only. Do not use any credentials or production data with the code here.
