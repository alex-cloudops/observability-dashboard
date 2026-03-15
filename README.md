# observability-dashboard

A production-grade observability dashboard that aggregates telemetry, uptime, incident, and log intelligence data from across a CloudOps ecosystem — transforming raw operational data into unified health scoring, structured JSON summaries, and Power BI ready exports.

Built as the crown jewel of the Alex-CloudOps observability portfolio.

---

## Overview

`observability-dashboard` is the central nervous system of the CloudOps portfolio ecosystem. It pulls data from all four portfolio repositories, transforms and scores each data source, calculates an overall ecosystem health status, and exports the results in multiple formats — including a Power BI ready dataset for executive-level visualization.

This project demonstrates senior-level CloudOps and observability engineering competencies:
- Multi-source data aggregation
- Metric transformation and health scoring
- Ecosystem-wide observability
- Power BI dataset generation
- CSV and JSON export pipelines

---

## Architecture
```
cloud-telemetry-agent  ──┐
synthetic-uptime-monitor ──┤
incident-alert-pipeline ──┤──▶ aggregator.py ──▶ transformer.py ──▶ summary.py ──▶ exporter.py
log-intelligence-engine ──┘                                                            │
                                                                                       ▼
                                                                          exports/dashboard_summary.json
                                                                          exports/dashboard_export.csv
                                                                          exports/powerbi_dataset.json
```

---

## Features

- **Multi-source aggregation** — Pulls data from all 4 portfolio repos
- **Health scoring** — HEALTHY, DEGRADED, CRITICAL per component and ecosystem
- **Unified dashboard view** — Single pane of glass across the entire ecosystem
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
| Exports | JSON, CSV |
| Visualization | Power BI Desktop (roadmap) |
| Configuration | configparser |

---

## Project Structure
```
observability-dashboard/
├── config/
│   ├── config.ini         # Dashboard configuration
│   └── sources.json       # Data source definitions
├── dashboard/
│   ├── __init__.py
│   ├── aggregator.py      # Multi-source data aggregation
│   ├── exporter.py        # JSON, CSV, Power BI exports
│   ├── summary.py         # Ecosystem health scoring
│   └── transformer.py     # Data transformation and normalization
├── data/
│   └── .gitkeep           # Live data files dropped here
├── exports/
│   └── .gitkeep           # Generated exports output here
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
- AWS account (Free Tier compatible)
- AWS CLI installed and configured

### Installation
```bash
git clone https://github.com/Alex-CloudOps/observability-dashboard.git
cd observability-dashboard
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Run the Dashboard
```bash
python main.py
```

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

## Power BI Integration

The `powerbi_dataset.json` export is structured for direct import into Power BI Desktop:
![CloudOps Observability Dashboard](assets/BI Dash.png)

1. Open Power BI Desktop
2. **Get Data** → **JSON**
3. Select `exports/powerbi_dataset.json`
4. Build visualizations using the pre-structured dataset

> Full Power BI dashboard development is on the roadmap.

---

## Ecosystem Integration

| Repository | Data Type | Metrics Provided |
|---|---|---|
| `cloud-telemetry-agent` | Telemetry | CPU, memory, disk |
| `synthetic-uptime-monitor` | Uptime | Availability, response times |
| `incident-alert-pipeline` | Incidents | Severity counts, open/closed |
| `log-intelligence-engine` | Log Intel | Error rates, health status |

---

## Roadmap

- [x] Unit tests with pytest
- [x] Multi-source data aggregation across all portfolio repos
- [x] Power BI Desktop dashboard with full visualizations
- [ ] Historical trending across multiple runs
- [ ] REST API endpoint for real-time dashboard queries
- [ ] Automated scheduled runs

---

## Author

**Alex Evans** | CloudOps & NOC Engineer
[GitHub](https://github.com/Alex-CloudOps) | alex.evans.cloudops@gmail.com

---

*The observability dashboard — where all five portfolio repositories converge into a single pane of glass. Built to demonstrate senior-level CloudOps and observability engineering practices.*