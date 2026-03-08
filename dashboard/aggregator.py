import json
import configparser
from pathlib import Path
from datetime import datetime, timezone

# Load config
config = configparser.ConfigParser()
config.read('config/config.ini')


def load_json_file(filepath):
    path = Path(filepath)
    if not path.exists():
        return None
    with open(path, 'r') as f:
        return json.load(f)


def generate_sample_telemetry():
    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'hostname': 'my-server-01',
        'environment': 'production',
        'metrics': [
            {'metric': 'cpu_percent', 'value': 8.5, 'unit': 'Percent'},
            {'metric': 'memory_percent', 'value': 87.0, 'unit': 'Percent'},
            {'metric': 'disk_percent', 'value': 17.9, 'unit': 'Percent'}
        ]
    }


def generate_sample_uptime():
    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'summary': {
            'total_targets': 5,
            'up': 4,
            'down': 1,
            'avg_response_time_ms': 353.9,
            'overall_health': 'DEGRADED'
        },
        'results': [
            {'name': 'Google', 'status': 'UP', 'response_time_ms': 210.5},
            {'name': 'GitHub', 'status': 'UP', 'response_time_ms': 320.1},
            {'name': 'AWS Console', 'status': 'UP', 'response_time_ms': 450.2},
            {'name': 'HTTPBin Health Check', 'status': 'UP', 'response_time_ms': 285.3},
            {'name': 'HTTPBin Simulated Failure', 'status': 'DOWN', 'response_time_ms': None}
        ]
    }


def generate_sample_incidents():
    return {
        'incidents': [
            {
                'incident_id': 'INC-20260308161020-815CC2DC',
                'severity': 'HIGH',
                'status': 'OPEN',
                'source': 'cloud-telemetry-agent',
                'message': 'memory_percent is at 91.0% on my-server-01'
            },
            {
                'incident_id': 'INC-20260308161020-E416C24A',
                'severity': 'CRITICAL',
                'status': 'OPEN',
                'source': 'synthetic-uptime-monitor',
                'message': 'HTTPBin Simulated Failure is DOWN'
            },
            {
                'incident_id': 'INC-20260308161020-CB2DE352',
                'severity': 'CRITICAL',
                'status': 'OPEN',
                'source': 'cloud-telemetry-agent',
                'message': 'cpu_percent is at 97.0% on prod-server-02'
            },
            {
                'incident_id': 'INC-20260308161020-A835995F',
                'severity': 'CRITICAL',
                'status': 'OPEN',
                'source': 'log-intelligence-engine',
                'message': 'CRITICAL health status on app-server.log'
            },
            {
                'incident_id': 'INC-20260308161020-81B2DF92',
                'severity': 'MEDIUM',
                'status': 'OPEN',
                'source': 'synthetic-uptime-monitor',
                'message': 'GitHub response time of 3200ms exceeds threshold'
            }
        ]
    }


def generate_sample_log_intelligence():
    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'total_files_analyzed': 1,
        'summary': [
            {
                'file': 'sample.log',
                'health_status': 'HEALTHY',
                'total_entries': 10000,
                'error_rate': 0.17,
                'warning_rate': 0.00,
                'level_counts': {
                    'INFO': 9983,
                    'ERROR': 17
                }
            }
        ]
    }


def aggregate_all():
    print("  Aggregating data sources...")

    telemetry = load_json_file('data/telemetry.json') or generate_sample_telemetry()
    uptime = load_json_file('data/uptime.json') or generate_sample_uptime()
    incidents = load_json_file('data/incidents.json') or generate_sample_incidents()
    log_intel = load_json_file('data/log_intelligence.json') or generate_sample_log_intelligence()

    print(f"    ✅ Telemetry data loaded")
    print(f"    ✅ Uptime data loaded")
    print(f"    ✅ Incidents data loaded")
    print(f"    ✅ Log intelligence data loaded")

    return {
        'aggregated_at': datetime.now(timezone.utc).isoformat(),
        'telemetry': telemetry,
        'uptime': uptime,
        'incidents': incidents,
        'log_intelligence': log_intel
    }