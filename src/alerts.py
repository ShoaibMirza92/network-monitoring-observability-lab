"""
alerts.py

Evaluate monitoring results against thresholds and return list of alerts.
"""

from typing import List, Dict, Any

SEVERITY_CRITICAL = "CRITICAL"
SEVERITY_WARNING = "WARNING"

def _make_alert(severity, device, metric, value, threshold, action):
    return {
        "severity": severity,
        "device": device,
        "metric": metric,
        "value": value,
        "threshold": threshold,
        "action": action
    }

def generate_alerts(results: List[Dict[str, Any]], thresholds: Dict[str, Any]) -> List[Dict[str, Any]]:
    alerts = []
    cpu_w = thresholds["cpu"]["warning"]
    cpu_c = thresholds["cpu"]["critical"]
    mem_w = thresholds["memory"]["warning"]
    mem_c = thresholds["memory"]["critical"]
    lat_w = thresholds["latency_ms"]["warning"]
    lat_c = thresholds["latency_ms"]["critical"]
    pl_w = thresholds["packet_loss"]["warning"]
    pl_c = thresholds["packet_loss"]["critical"]

    for r in results:
        host = r.get("hostname")
        if r.get("status") != "UP":
            alerts.append(_make_alert(SEVERITY_CRITICAL, host, "availability", r.get("status"), "UP",
                                      "Verify device power, management network, or console access"))
            continue
        # CPU
        cpu = r.get("cpu")
        if cpu is not None:
            if cpu >= cpu_c:
                alerts.append(_make_alert(SEVERITY_CRITICAL, host, "cpu", cpu, cpu_c,
                                          "Investigate process & traffic spikes; consider maintenance"))
            elif cpu >= cpu_w:
                alerts.append(_make_alert(SEVERITY_WARNING, host, "cpu", cpu, cpu_w,
                                          "Monitor CPU usage; check routes and recent changes"))
        # Memory
        mem = r.get("memory")
        if mem is not None:
            if mem >= mem_c:
                alerts.append(_make_alert(SEVERITY_CRITICAL, host, "memory", mem, mem_c,
                                          "Investigate memory leaks; plan reboot or patch"))
            elif mem >= mem_w:
                alerts.append(_make_alert(SEVERITY_WARNING, host, "memory", mem, mem_w,
                                          "Monitor memory; reduce load"))
        # Latency
        lat = r.get("latency_ms")
        if lat is not None:
            if lat >= lat_c:
                alerts.append(_make_alert(SEVERITY_CRITICAL, host, "latency_ms", lat, lat_c,
                                          "Investigate routing, QoS, or link issues"))
            elif lat >= lat_w:
                alerts.append(_make_alert(SEVERITY_WARNING, host, "latency_ms", lat, lat_w,
                                          "Monitor latency; review path/trend"))
        # Packet loss
        pl = r.get("packet_loss")
        if pl is not None:
            if pl >= pl_c:
                alerts.append(_make_alert(SEVERITY_CRITICAL, host, "packet_loss", pl, pl_c,
                                          "Check interfaces, cabling, and congestion"))
            elif pl >= pl_w:
                alerts.append(_make_alert(SEVERITY_WARNING, host, "packet_loss", pl, pl_w,
                                          "Monitor for increasing packet loss; check counters"))
        # Interfaces
        for iface in r.get("interfaces", []):
            if iface.get("status") != "UP":
                alerts.append(_make_alert(SEVERITY_CRITICAL, host, f"interface::{iface.get('name')}", iface.get("status"), "UP",
                                          "Investigate interface: check cable, SFP, or switch port configuration"))
    return alerts
