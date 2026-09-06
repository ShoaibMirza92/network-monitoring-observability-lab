import json
from pathlib import Path
from src import monitor, alerts, reporting

def test_load_devices_and_thresholds():
    devices = monitor.load_devices()
    thresholds = monitor.load_thresholds()
    assert isinstance(devices, list)
    assert len(devices) >= 1
    assert "hostname" in devices[0]
    assert "cpu" in thresholds

def test_run_monitor_deterministic():
    payload1 = monitor.run_monitor(seed=101)
    payload2 = monitor.run_monitor(seed=101)
    assert payload1["results"] == payload2["results"]

def test_alert_generation_on_high_cpu():
    thresholds = monitor.load_thresholds()
    high_cpu_metric = [{
        "hostname": "TEST-RTR",
        "management_ip": "10.10.99.1",
        "device_type": "router",
        "location": "lab",
        "environment": "test",
        "status": "UP",
        "cpu": 95.0,
        "memory": 30.0,
        "interfaces": [],
        "packet_loss": 0.0,
        "latency_ms": 10
    }]
    al = alerts.generate_alerts(high_cpu_metric, thresholds)
    assert any(a for a in al if a["metric"] == "cpu" and a["severity"] == "CRITICAL")

def test_reporting_writes_csv(tmp_path):
    payload = monitor.run_monitor(seed=202)
    al = alerts.generate_alerts(payload["results"], payload["thresholds"])
    csv_path = tmp_path / "out.csv"
    reporting.write_csv_report(payload["results"], al, csv_path)
    assert csv_path.exists()
    lines = csv_path.read_text().splitlines()
    assert "hostname" in lines[0]
