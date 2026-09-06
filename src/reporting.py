"""
reporting.py

Produce a console report (and optional CSV).
"""

from typing import List, Dict, Any
from pathlib import Path
import csv
import datetime

def print_report(results: List[Dict[str, Any]], alerts: List[Dict[str, Any]], write_csv: bool = True, csv_path: Path | None = None):
    total = len(results)
    healthy = sum(1 for r in results if r.get("status") == "UP" and not any(a for a in alerts if a["device"] == r["hostname"] and a["severity"] == "CRITICAL"))
    warnings = sum(1 for a in alerts if a["severity"] == "WARNING")
    criticals = sum(1 for a in alerts if a["severity"] == "CRITICAL")
    print("="*60)
    print("Network Monitoring Report (simulated)")
    print("Timestamp:", datetime.datetime.utcnow().isoformat())
    print(f"Total devices: {total}")
    print(f"Healthy devices (no critical alerts): {healthy}")
    print(f"Warning alerts: {warnings}")
    print(f"Critical alerts: {criticals}")
    print("-"*60)
    for r in results:
        host = r["hostname"]
        status = r.get("status")
        cpu = r.get("cpu") or ""
        mem = r.get("memory") or ""
        lat = r.get("latency_ms") or ""
        pl = r.get("packet_loss") or ""
        print(f"{host:20} {status:6} CPU:{str(cpu):>6} MEM:{str(mem):>6} LAT:{str(lat):>4}ms PL:{str(pl):>5}%")
    print("-"*60)
    if alerts:
        print("Alerts:")
        for a in alerts:
            print(f"[{a['severity']}] {a['device']} - {a['metric']} = {a['value']} (thr: {a['threshold']}) -> {a['action']}")
    else:
        print("No alerts.")
    print("="*60)
    if write_csv:
        csv_path = csv_path or (Path.cwd() / "report_network_monitoring.csv")
        write_csv_report(results, alerts, csv_path)
        print(f"CSV report written to: {csv_path}")

def write_csv_report(results: List[Dict[str, Any]], alerts: List[Dict[str, Any]], path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    sev_map = {}
    for a in alerts:
        dev = a["device"]
        prev = sev_map.get(dev)
        level = 2 if a["severity"] == "CRITICAL" else 1
        if prev is None or level > prev[0]:
            sev_map[dev] = (level, a["severity"])
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp","hostname","management_ip","status","cpu","memory","latency_ms","packet_loss","severity"])
        ts = datetime.datetime.utcnow().isoformat()
        for r in results:
            severity = sev_map.get(r["hostname"], (0,"OK"))[1] if sev_map.get(r["hostname"]) else "OK"
            writer.writerow([ts, r["hostname"], r["management_ip"], r["status"], r.get("cpu") or "", r.get("memory") or "", r.get("latency_ms") or "", r.get("packet_loss") or "", severity])
