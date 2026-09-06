```mermaid
flowchart TD
  Internet[Internet]
  FW[FIREWALL-01\n172.16.10.1]
  EDGE[EDGE-RTR-01\n192.168.10.1]
  CORE[CORE-RTR-01\n10.10.1.1]
  CORESW[CORE-SW-01\n10.10.1.2]
  DIST[DIST-SW-01\n10.10.2.10]
  ACCESS[ACCESS-SW-01\n10.10.3.5]
  MON[Monitoring Collector]

  Internet --> FW --> EDGE --> CORE --> CORESW --> DIST --> ACCESS
  CORE <-- MON
  CORESW <-- MON
  DIST <-- MON
  EDGE <-- MON
  FW <-- MON
  ACCESS <-- MON
```
