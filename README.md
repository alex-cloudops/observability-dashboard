# observability-dashboard

A production-grade observability dashboard that aggregates telemetry, uptime, incident, and log intelligence data from across a CloudOps ecosystem — transforming raw operational data into unified health scoring, structured JSON summaries, Power BI ready exports, and a live Grafana dashboard powered by Prometheus.

Built as the crown jewel of the Alex-CloudOps observability portfolio.

---

## Overview

`observability-dashboard` is the central nervous system of the CloudOps portfolio ecosystem. It pulls data from all four portfolio repositories, transforms and scores each data source, calculates an overall ecosystem health status, and exports the results in multiple formats — including a live Grafana dashboard with real-time metric visualization.

This project demonstrates senior-level CloudOps and observability engineering competencies:
- Multi-source data aggregation
- Metric transformation and health scoring
- Ecosystem-wide observability
- Live Prometheus metrics exposition
- Grafana dashboard with NOC-grade threshold alerting
- Power BI dataset generation
- CSV and JSON export pipelines

---

## Architecture
```
cloud-telemetry-agent  ──┐
synthetic-uptime-monitor ──┤
incident-alert-pipeline ──┤──▶ aggregator.py ──▶ transformer.py ──▶ summary.py ──▶ exporter.py
log-intelligence-engine ──┘                │
                                           ▼
                                  metrics_exporter.py
                                           │
                                           ▼
                                  Prometheus (port 9090)
                                           │
                                           ▼
                                  Grafana Dashboard (port 3000)
```

---

## Features

- **Multi-source aggregation** — Pulls data from all 4 portfolio repos
- **Health scoring** — HEALTHY, DEGRADED, CRITICAL per component and ecosystem
- **Unified dashboard view** — Single pane of glass across the entire ecosystem
- **Live Prometheus metrics** — Real-time metrics exposition on port 8000
- **Grafana dashboard** — 8-panel NOC dashboard with threshold-based color alerting
- **Power BI ready exports** — JSON dataset and CSV for direct Power BI import
- **Config-driven sources** — Add or disable data sources via `sources.json`
- **Zero hardcoded values** — All configuration via `config.ini`

---

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.x |
| AWS SDK | boto3 / botocore |
| HTTP | requests |
| Metrics Exposition | prometheus-client |
| Metrics Collection | Prometheus |
| Visualization | Grafana |
| Exports | JSON, CSV |
| Configuration | configparser |

---

## Project Structure
```
observability-dashboard/
├── config/
│   ├── config.ini             # Dashboard configuration
│   └── sources.json           # Data source definitions
├── dashboard/
│   ├── __init__.py
│   ├── aggregator.py          # Multi-source data aggregation
│   ├── exporter.py            # JSON, CSV, Power BI exports
│   ├── metrics_exporter.py    # Prometheus metrics exposition
│   ├── summary.py             # Ecosystem health scoring
│   └── transformer.py         # Data transformation and normalization
├── data/
│   └── .gitkeep               # Live data files dropped here
├── exports/
│   └── .gitkeep               # Generated exports output here
├── grafana/
│   └── dashboard.json         # Grafana dashboard — importable
├── logs/
│   └── .gitkeep
├── tests/
│   └── __init__.py
├── requirements.txt
└── main.py
```

---

## Getting Started

### Prerequisites
- Python 3.8+
- Prometheus
- Grafana
- AWS account (Free Tier compatible)
- AWS CLI installed and configured

### Installation
```bash
git clone https://github.com/Alex-CloudOps/observability-dashboard.git
cd observability-dashboard
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Run the Metrics Exporter
```bash
python -m dashboard.metrics_exporter
```
Metrics will be available at `http://localhost:8000/metrics`

### Run Prometheus
```bash
prometheus --config.file=prometheus.yml
```
Prometheus UI available at `http://localhost:9090`

### Import the Grafana Dashboard
1. Open Grafana at `http://localhost:3000`
2. Go to **Dashboards** → **Import**
3. Upload `grafana/dashboard.json`
4. Select your Prometheus data source
5. Click **Import**

### Run the Dashboard Export Pipeline
```bash
python main.py
```

---

## Grafana Dashboard

The included Grafana dashboard provides 8 live panels with NOC-grade threshold alerting:

| Panel | Metric | Thresholds |
|---|---|---|
| CPU Usage % | `cloudops_cpu_percent` | Green < 75, Yellow < 90, Red ≥ 90 |
| Memory Usage % | `cloudops_memory_percent` | Green < 90, Yellow < 95, Red ≥ 95 |
| Disk Usage % | `cloudops_disk_percent` | Green < 85, Yellow < 90, Red ≥ 90 |
| Uptime % | `cloudops_uptime_percent` | Red < 90, Yellow < 99, Green ≥ 99 |
| Avg Response Time | `cloudops_avg_response_time_ms` | Green < 2000ms, Yellow < 4000ms, Red ≥ 4000ms |
| Open Incidents | `cloudops_open_incidents` | Green = 0, Yellow ≥ 1, Red ≥ 5 |
| Critical Incidents | `cloudops_critical_incidents` | Green = 0, Orange ≥ 1, Red ≥ 3 |
| Log Error Rate % | `cloudops_log_error_rate` | Green < 5, Yellow < 10, Red ≥ 10 |

---

## Sample Output
```
============================================================
  OBSERVABILITY DASHBOARD
============================================================
🚨 ECOSYSTEM HEALTH: CRITICAL
============================================================
  📊 Component Health:
    Telemetry    : ✅ HEALTHY
    Uptime       : ⚠️ DEGRADED
    Log Intel    : ✅ HEALTHY

  📈 Key Metrics:
    CPU          : 8.5%
    Memory       : 87.0%
    Disk         : 17.9%
    Uptime       : 80.0%
    Avg Response : 353.9ms
    Log Errors   : 0.17%

  🚨 Incidents:
    Open         : 5
    Critical     : 3
    Total        : 5
============================================================
```

---

## Exports

Every run generates three export files in `exports/`:

| File | Format | Purpose |
|---|---|---|
| `dashboard_summary.json` | JSON | Full ecosystem summary |
| `dashboard_export.csv` | CSV | Flat metric export for analysis |
| `powerbi_dataset.json` | JSON | Structured Power BI import dataset |

---

## Ecosystem Integration

| Repository | Data Type | Metrics Provided |
|---|---|---|
| `cloud-telemetry-agent` | Telemetry | CPU, memory, disk |
| `synthetic-uptime-monitor` | Uptime | Availability, response times |
| `incident-alert-pipeline` | Incidents | Severity counts, open/closed |
| `log-intelligence-engine` | Log Intel | Error rates, health status |

---
## Live Data Sources

The metrics exporter collects all 8 Prometheus metrics from live sources — zero sample data, zero fallback.

| Metric | Source | Method |
|---|---|---|
| CPU Usage % | Local machine | psutil |
| Memory Usage % | Local machine | psutil |
| Disk Usage % | Local machine | psutil |
| Uptime % | 5 live HTTP targets | requests |
| Avg Response Time | 5 live HTTP targets | requests |
| Open Incidents | AWS CloudWatch Alarms | boto3 |
| Critical Incidents | AWS CloudWatch Alarms | boto3 |
| Log Error Rate | logs/dashboard.log | Python file scan |

### CloudWatch Alarms
Three alarms are configured in AWS CloudWatch (us-east-2) and queried in real time:

| Alarm | Metric | Threshold |
|---|---|---|
| `cloudops-cpu-critical` | cpu_percent | ≥ 90% |
| `cloudops-memory-critical` | memory_percent | ≥ 95% |
| `cloudops-disk-critical` | disk_percent | ≥ 90% |

When any alarm enters ALARM state, the incident counters in Grafana increment automatically.

## Roadmap

- [x] Multi-source data aggregation
- [x] Ecosystem health scoring
- [x] JSON, CSV, Power BI exports
- [x] Prometheus metrics exposition
- [x] Grafana dashboard with NOC-grade thresholds
- [x] Live data pipeline from all portfolio repos
- [ ] Historical trending across multiple runs
- [ ] REST API endpoint for real-time dashboard queries
- [ ] Automated scheduled runs
- [ ] Unit tests with pytest

---

## Author

**Alex Evans** | CloudOps & NOC Engineer
[GitHub](https://github.com/Alex-CloudOps) | alex.evans.cloudops@gmail.com

---

*The observability dashboard — where all five portfolio repositories converge into a single pane of glass. Built to demonstrate senior-level CloudOps and observability engineering practices.*