import json
import csv
import configparser
from pathlib import Path
from datetime import datetime, timezone

# Load config
config = configparser.ConfigParser()
config.read('config/config.ini')

SUMMARY_FILE = config['exports']['summary_file']
CSV_FILE = config['exports']['csv_file']
POWERBI_FILE = config['exports']['powerbi_file']


def export_summary(summary):
    path = Path(SUMMARY_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(summary, f, indent=4)
    print(f"    ✅ Summary exported → {SUMMARY_FILE}")


def export_csv(transformed):
    path = Path(CSV_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    timestamp = datetime.now(timezone.utc).isoformat()

    # Telemetry rows
    telemetry = transformed['telemetry']
    rows.append({
        'timestamp': timestamp,
        'source': 'cloud-telemetry-agent',
        'metric': 'cpu_percent',
        'value': telemetry['cpu_percent'],
        'unit': 'Percent',
        'status': telemetry['health_status']
    })
    rows.append({
        'timestamp': timestamp,
        'source': 'cloud-telemetry-agent',
        'metric': 'memory_percent',
        'value': telemetry['memory_percent'],
        'unit': 'Percent',
        'status': telemetry['health_status']
    })
    rows.append({
        'timestamp': timestamp,
        'source': 'cloud-telemetry-agent',
        'metric': 'disk_percent',
        'value': telemetry['disk_percent'],
        'unit': 'Percent',
        'status': telemetry['health_status']
    })

    # Uptime rows
    uptime = transformed['uptime']
    for target in uptime['targets']:
        rows.append({
            'timestamp': timestamp,
            'source': 'synthetic-uptime-monitor',
            'metric': target['name'],
            'value': target['response_time_ms'] or 0,
            'unit': 'Milliseconds',
            'status': target['status']
        })

    # Incident rows
    incidents = transformed['incidents']
    rows.append({
        'timestamp': timestamp,
        'source': 'incident-alert-pipeline',
        'metric': 'open_incidents',
        'value': incidents['open'],
        'unit': 'Count',
        'status': 'OPEN' if incidents['open'] > 0 else 'CLEAR'
    })

    # Log intelligence rows
    log_intel = transformed['log_intelligence']
    rows.append({
        'timestamp': timestamp,
        'source': 'log-intelligence-engine',
        'metric': 'error_rate',
        'value': log_intel['error_rate'],
        'unit': 'Percent',
        'status': log_intel['health_status']
    })

    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'timestamp', 'source', 'metric', 'value', 'unit', 'status'
        ])
        writer.writeheader()
        writer.writerows(rows)

    print(f"    ✅ CSV exported → {CSV_FILE}")


def export_powerbi(summary, transformed):
    """
    Exports a Power BI ready dataset — structured for direct
    import into Power BI Desktop as a JSON data source.
    """
    powerbi_dataset = {
        'dataset_name': 'CloudOps Observability Dashboard',
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'overall_health': summary['overall_health'],
        'telemetry': {
            'hostname': transformed['telemetry']['hostname'],
            'environment': transformed['telemetry']['environment'],
            'cpu_percent': transformed['telemetry']['cpu_percent'],
            'memory_percent': transformed['telemetry']['memory_percent'],
            'disk_percent': transformed['telemetry']['disk_percent'],
            'health_status': transformed['telemetry']['health_status']
        },
        'uptime': {
            'total_targets': transformed['uptime']['total_targets'],
            'up': transformed['uptime']['up'],
            'down': transformed['uptime']['down'],
            'uptime_percent': transformed['uptime']['uptime_percent'],
            'avg_response_time_ms': transformed['uptime']['avg_response_time_ms'],
            'targets': transformed['uptime']['targets']
        },
        'incidents': {
            'total': transformed['incidents']['total_incidents'],
            'open': transformed['incidents']['open'],
            'closed': transformed['incidents']['closed'],
            'critical': transformed['incidents']['severity_counts'].get('CRITICAL', 0),
            'high': transformed['incidents']['severity_counts'].get('HIGH', 0),
            'medium': transformed['incidents']['severity_counts'].get('MEDIUM', 0),
            'low': transformed['incidents']['severity_counts'].get('LOW', 0)
        },
        'log_intelligence': {
            'file': transformed['log_intelligence']['file'],
            'health_status': transformed['log_intelligence']['health_status'],
            'total_entries': transformed['log_intelligence']['total_entries'],
            'error_rate': transformed['log_intelligence']['error_rate'],
            'warning_rate': transformed['log_intelligence']['warning_rate']
        }
    }

    path = Path(POWERBI_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(powerbi_dataset, f, indent=4)

    print(f"    ✅ Power BI dataset exported → {POWERBI_FILE}")
    return powerbi_dataset


def export_all(summary, transformed):
    print("  Exporting outputs...")
    export_summary(summary)
    export_csv(transformed)
    export_powerbi(summary, transformed)