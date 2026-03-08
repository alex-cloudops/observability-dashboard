from datetime import datetime, timezone


def generate_summary(transformed):
    telemetry = transformed['telemetry']
    uptime = transformed['uptime']
    incidents = transformed['incidents']
    log_intel = transformed['log_intelligence']

    # Overall ecosystem health score
    health_scores = {
        'HEALTHY': 0,
        'DEGRADED': 1,
        'CRITICAL': 2
    }

    scores = [
        health_scores.get(telemetry.get('health_status', 'HEALTHY'), 0),
        health_scores.get(uptime.get('overall_health', 'HEALTHY'), 0),
        health_scores.get(log_intel.get('health_status', 'HEALTHY'), 0)
    ]

    if incidents.get('critical_open', 0) > 0:
        scores.append(2)

    max_score = max(scores)
    if max_score == 2:
        overall_health = 'CRITICAL'
    elif max_score == 1:
        overall_health = 'DEGRADED'
    else:
        overall_health = 'HEALTHY'

    summary = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'overall_health': overall_health,
        'ecosystem': {
            'telemetry_health': telemetry.get('health_status'),
            'uptime_health': uptime.get('overall_health'),
            'log_health': log_intel.get('health_status'),
            'open_incidents': incidents.get('open', 0),
            'critical_incidents': incidents.get('critical_open', 0)
        },
        'metrics': {
            'cpu_percent': telemetry.get('cpu_percent'),
            'memory_percent': telemetry.get('memory_percent'),
            'disk_percent': telemetry.get('disk_percent'),
            'uptime_percent': uptime.get('uptime_percent'),
            'avg_response_time_ms': uptime.get('avg_response_time_ms'),
            'log_error_rate': log_intel.get('error_rate')
        },
        'incidents': {
            'total': incidents.get('total_incidents', 0),
            'open': incidents.get('open', 0),
            'closed': incidents.get('closed', 0),
            'by_severity': incidents.get('severity_counts', {})
        }
    }

    return summary


def print_summary(summary):
    health_icons = {
        'HEALTHY': '✅',
        'DEGRADED': '⚠️',
        'CRITICAL': '🚨'
    }

    overall = summary['overall_health']
    icon = health_icons.get(overall, '❓')
    ecosystem = summary['ecosystem']
    metrics = summary['metrics']
    incidents = summary['incidents']

    print("\n" + "=" * 60)
    print(f"  {icon} ECOSYSTEM HEALTH: {overall}")
    print("=" * 60)

    print("\n  📊 Component Health:")
    print(f"    Telemetry    : {health_icons.get(ecosystem['telemetry_health'], '❓')} {ecosystem['telemetry_health']}")
    print(f"    Uptime       : {health_icons.get(ecosystem['uptime_health'], '❓')} {ecosystem['uptime_health']}")
    print(f"    Log Intel    : {health_icons.get(ecosystem['log_health'], '❓')} {ecosystem['log_health']}")

    print("\n  📈 Key Metrics:")
    print(f"    CPU          : {metrics['cpu_percent']}%")
    print(f"    Memory       : {metrics['memory_percent']}%")
    print(f"    Disk         : {metrics['disk_percent']}%")
    print(f"    Uptime       : {metrics['uptime_percent']}%")
    print(f"    Avg Response : {metrics['avg_response_time_ms']}ms")
    print(f"    Log Errors   : {metrics['log_error_rate']}%")

    print("\n  🚨 Incidents:")
    print(f"    Open         : {incidents['open']}")
    print(f"    Critical     : {incidents['by_severity'].get('CRITICAL', 0)}")
    print(f"    High         : {incidents['by_severity'].get('HIGH', 0)}")
    print(f"    Medium       : {incidents['by_severity'].get('MEDIUM', 0)}")
    print(f"    Total        : {incidents['total']}")
    print("=" * 60)