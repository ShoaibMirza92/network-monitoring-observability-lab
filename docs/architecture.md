# Architecture

This lab simulates a monitoring pipeline:

- Devices (simulated) provide management interfaces and telemetry.
- src.monitor loads device inventory and thresholds, simulates availability & metrics.
- src.alerts evaluates thresholds and generates actionable alerts.
- src.reporting prints a summary and writes a CSV report.

All telemetry is simulated locally with deterministic seeds for testability.
