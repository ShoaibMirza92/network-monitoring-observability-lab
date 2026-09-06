# Troubleshooting Scenarios

1. Device unreachable
- Problem: Device returns no ICMP response.
- Possible causes: power/cabling, management VLAN down, ACL blocking.
- Investigation: ping, traceroute, check interface LEDs/console.
- Expected finding: device down or management IP unreachable.
- Resolution: fix power/cable, adjust ACLs, restore management path.

2. High CPU utilization
- Problem: CPU above critical threshold.
- Possible causes: control-plane attack, routing loops, process runaway.
- Investigation: show processes cpu, check interface counters, recent config changes.
- Expected: one process consuming CPU or sudden traffic spike.
- Resolution: mitigate process, apply rate-limit, schedule maintenance.

3. High memory utilization
- Problem: Memory above threshold.
- Possible causes: memory leak, too many sessions, faulty process.
- Investigation: show memory, logs.
- Resolution: restart process, patch, or scale resources.

4. High network latency
- Problem: Latency > threshold causing application performance issues.
- Possible causes: congestion, sub-optimal routing, interface errors.
- Investigation: traceroute, check interface errors, QoS config.
- Resolution: relieve congestion, re-route, fix interfaces, apply QoS.

5. Interface down
- Problem: An interface status is DOWN.
- Possible causes: physical fault, SFP/cable, admin down.
- Investigation: show interfaces, physical inspection.
- Resolution: replace cabling/SFP, enable interface, verify config.
