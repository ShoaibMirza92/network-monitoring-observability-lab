"""
monitor.py

Load config, simulate monitoring results deterministically (seeded),
and produce structured monitoring results for alerts and reporting.

Run as module:
  python -m src.monitor
"""

from pathlib import Path
import json
import random
from typing import List, Dict, Any
import sys

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"
DEVICES_FILE = CONFIG_DIR / "devices.json"
THRESHOLDS_FILE = CONFIG_DIR / "thresholds.json"

def load_json(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def load_devices(path: Path = DEVICES_FILE) -> List[Dict[str, Any]]:
    return load_json(path)

def load_thresholds(path: Path = THRESHOLDS_FILE) -> Dict[str, Any]:
    return load_json(path)

def simulate_availability(rng: random.Random, down_prob: float) -> bool:
    return rng.random() >= down_prob

def simulate_interface_statuses(rng: random.Random, interfaces: List[str], down_prob: float):
    out = []
    for iface in interfaces:
        up = rng.random() >= down_prob
        util = None
        if up:
            util = round(max(0.0, min(100.0, rng.gauss(10.0, 10.0))), 1)
        out.append({"name": iface, "status": "UP" if up else "DOWN", "utilization_percent": util})
    return out

def simulate_metrics_for_device(rng: random.Random, device: Dict[str, Any], thresholds: Dict[str, Any]) -> Dict[str, Any]:
    down_prob = thresholds.get("device_down_prob", 0.03)
    iface_down_prob = thresholds.get("interface_down_prob", 0.02)
    is_up = simulate_availability(rng, down_prob)
    if not is_up:
        return {
            "hostname": device["hostname"],
            "management_ip": device["management_ip"],
            "device_type": device["device_type"],
            "location": device["location"],
            "environment": device["environment"],
            "status": "DOWN",
            "cpu": None,
            "memory": None,
            "interfaces": simulate_interface_statuses(rng, device.get("interfaces", []), 1.0),
            "packet_loss": None,
            "latency_ms": None
        }
    dtype = device.get("device_type", "").lower()
    if dtype == "router":
        cpu_base = 25
        mem_base = 30
        lat_base = 15
    elif dtype == "switch":
        cpu_base = 10
        mem_base = 20
        lat_base = 5
    elif dtype == "firewall":
        cpu_base = 35
        mem_base = 40
        lat_base = 25
    else:
        cpu_base = 20
        mem_base = 30
        lat_base = 10

    cpu = round(max(0.0, min(100.0, rng.gauss(cpu_base, cpu_base*0.3))), 1)
    memory = round(max(0.0, min(100.0, rng.gauss(mem_base, mem_base*0.25))), 1)
    interfaces = simulate_interface_statuses(rng, device.get("interfaces", []), iface_down_prob)
    packet_loss = round(max(0.0, rng.gauss(0.1, 1.0)), 2)
    latency = max(1, int(rng.gauss(lat_base, lat_base*0.25)))
    return {
        "hostname": device["hostname"],
        "management_ip": device["management_ip"],
        "device_type": device["device_type"],
        "location": device["location"],
        "environment": device["environment"],
        "status": "UP",
        "cpu": cpu,
        "memory": memory,
        "interfaces": interfaces,
        "packet_loss": packet_loss,
        "latency_ms": latency
    }

def run_monitor(seed: int = 12345) -> Dict[str, Any]:
    devices = load_devices()
    thresholds = load_thresholds()
    rng = random.Random(seed)
    results = []
    for d in devices:
        results.append(simulate_metrics_for_device(rng, d, thresholds))
    return {"devices": devices, "thresholds": thresholds, "results": results}

def main():
    try:
        payload = run_monitor()
    except Exception as e:
        print(f"Monitoring run failed: {e}", file=sys.stderr)
        sys.exit(2)
    from src import alerts, reporting
    alerts_list = alerts.generate_alerts(payload["results"], payload["thresholds"])
    reporting.print_report(payload["results"], alerts_list)
    return 0

if __name__ == "__main__":
    main()
