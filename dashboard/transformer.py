from datetime import datetime, timezone


def transform_telemetry(telemetry):
    metrics = {m['metric']: m['value'] for m in telemetry.get('metrics', [])}
    return {
        'hostname': telemetry.get('hostname', 'unknown'),
        'environment': telemetry.get('environment', 'unknown'),
        'cpu_percent': metrics.get('cpu_percent', 0),
        'memory_percent': metrics.get('memory_percent', 0),
        'disk_percent': metrics.get('disk_percent', 0),
        'health_status': _score_telemetry_health(metrics)
    }


def _score_telemetry_health(metrics):
    cpu = metrics.get('cpu_percent', 0)
    memory = metrics.get('memory_percent', 0)
    disk = metrics.get('disk_percent', 0)

    if cpu >= 95 or memory >= 95 or disk >= 95:
        return 'CRITICAL'
    elif cpu >= 85 or memory >= 90 or disk >= 90:
        return 'DEGRADED'
    return 'HEALTHY'


def transform_uptime(uptime):
    summary = uptime.get('summary', {})
    results = uptime.get('results', [])

    return {
        'total_targets': summary.get('total_targets', 0),
        'up': summary.get('up', 0),
        'down': summary.get('down', 0),
        'avg_response_time_ms': summary.get('avg_response_time_ms', 0),
        'overall_health': summary.get('overall_health', 'UNKNOWN'),
        'uptime_percent': round(
            summary.get('up', 0) / summary.get('total_targets', 1) * 100, 2
        ),
        'targets': [
            {
                'name': r['name'],
                'status': r['status'],
                'response_time_ms': r.get('response_time_ms')
            }
            for r in results
        ]
    }


def transform_incidents(incidents_data):
    incidents = incidents_data.get('incidents', [])
    total = len(incidents)
    open_count = sum(1 for i in incidents if i['status'] == 'OPEN')
    closed_count = sum(1 for i in incidents if i['status'] == 'CLOSED')

    severity_counts = {
        'CRITICAL': sum(1 for i in incidents if i['severity'] == 'CRITICAL'),
        'HIGH': sum(1 for i in incidents if i['severity'] == 'HIGH'),
        'MEDIUM': sum(1 for i in incidents if i['severity'] == 'MEDIUM'),
        'LOW': sum(1 for i in incidents if i['severity'] == 'LOW')
    }

    return {
        'total_incidents': total,
        'open': open_count,
        'closed': closed_count,
        'severity_counts': severity_counts,
        'critical_open': sum(
            1 for i in incidents
            if i['severity'] == 'CRITICAL' and i['status'] == 'OPEN'
        )
    }


def transform_log_intelligence(log_data):
    summaries = log_data.get('summary', [])
    if not summaries:
        return {}

    summary = summaries[0]
    return {
        'file': summary.get('file', 'unknown'),
        'health_status': summary.get('health_status', 'UNKNOWN'),
        'total_entries': summary.get('total_entries', 0),
        'error_rate': summary.get('error_rate', 0),
        'warning_rate': summary.get('warning_rate', 0),
        'level_counts': summary.get('level_counts', {})
    }


def transform_all(aggregated):
    print("  Transforming data...")
    transformed = {
        'transformed_at': datetime.now(timezone.utc).isoformat(),
        'telemetry': transform_telemetry(aggregated['telemetry']),
        'uptime': transform_uptime(aggregated['uptime']),
        'incidents': transform_incidents(aggregated['incidents']),
        'log_intelligence': transform_log_intelligence(aggregated['log_intelligence'])
    }
    print("    ✅ All sources transformed")
    return transformed