# Network Monitoring & Observability Lab

Overview
This is a simulated Network Monitoring & Observability Lab for portfolio and training purposes. It demonstrates device availability monitoring, simulated ICMP/latency, CPU/memory metrics, interface status, packet-loss detection, threshold-based alerting, reporting, and unit testing — all with simulated data. No real network devices or credentials are used.

Quick start (Windows PowerShell)
1. Create venv and activate
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
2. Install dependencies
   pip install -r requirements.txt
3. Run the monitor
   python -m src.monitor
4. Run tests
   pytest -q

Project structure
- config/: device inventory and thresholds
- src/: Python monitoring modules (monitor, alerts, reporting)
- tests/: pytest unit tests
- docs/: architecture and troubleshooting scenarios
- diagrams/: network topology (Mermaid)

Disclaimer
This is a simulated lab. It does not connect to real devices or use real credentials. SNMP and syslog are documented as concepts only.
