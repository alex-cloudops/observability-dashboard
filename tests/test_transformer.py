import pytest
from dashboard.transformer import (
    transform_telemetry,
    transform_uptime,
    transform_incidents,
    transform_log_intelligence,
    transform_all
)


def make_telemetry(cpu=10.0, memory=50.0, disk=30.0, hostname='test-server', environment='production'):
    """Helper — build a raw telemetry payload."""
    return {
        'hostname': hostname,
        'environment': environment,
        'metrics': [
            {'metric': 'cpu_percent', 'value': cpu, 'unit': 'Percent'},
            {'metric': 'memory_percent', 'value': memory, 'unit': 'Percent'},
            {'metric': 'disk_percent', 'value': disk, 'unit': 'Percent'},
        ]
    }


def make_uptime(total=5, up=4, down=1, avg_response=300.0, health='DEGRADED'):
    """Helper — build a raw uptime payload."""
    return {
        'summary': {
            'total_targets': total,
            'up': up,
            'down': down,
            'avg_response_time_ms': avg_response,
            'overall_health': health
        },
        'results': [
            {'name': 'Google', 'status': 'UP', 'response_time_ms': 210.0},
            {'name': 'GitHub', 'status': 'DOWN', 'response_time_ms': None},
        ]
    }


def make_incidents(incident_list=None):
    """Helper — build a raw incidents payload."""
    return {'incidents': incident_list or []}


def make_log_intelligence(file='test.log', health='HEALTHY', total=1000, error_rate=0.5, warning_rate=1.0):
    """Helper — build a raw log intelligence payload."""
    return {
        'summary': [{
            'file': file,
            'health_status': health,
            'total_entries': total,
            'error_rate': error_rate,
            'warning_rate': warning_rate,
            'level_counts': {'INFO': 990, 'ERROR': 10}
        }]
    }


class TestTransformTelemetry:
    def test_returns_required_fields(self):
        result = transform_telemetry(make_telemetry())
        for field in ['hostname', 'environment', 'cpu_percent', 'memory_percent', 'disk_percent', 'health_status']:
            assert field in result, f"Missing field: {field}"

    def test_hostname_is_correct(self):
        result = transform_telemetry(make_telemetry(hostname='prod-server-01'))
        assert result['hostname'] == 'prod-server-01'

    def test_cpu_value_is_correct(self):
        result = transform_telemetry(make_telemetry(cpu=42.5))
        assert result['cpu_percent'] == 42.5

    def test_memory_value_is_correct(self):
        result = transform_telemetry(make_telemetry(memory=78.0))
        assert result['memory_percent'] == 78.0

    def test_disk_value_is_correct(self):
        result = transform_telemetry(make_telemetry(disk=55.0))
        assert result['disk_percent'] == 55.0


class TestTelemetryHealthScoring:
    def test_healthy_when_all_metrics_normal(self):
        result = transform_telemetry(make_telemetry(cpu=10.0, memory=50.0, disk=30.0))
        assert result['health_status'] == 'HEALTHY'

    def test_critical_when_cpu_at_95(self):
        result = transform_telemetry(make_telemetry(cpu=95.0))
        assert result['health_status'] == 'CRITICAL'

    def test_critical_when_memory_at_95(self):
        result = transform_telemetry(make_telemetry(memory=95.0))
        assert result['health_status'] == 'CRITICAL'

    def test_critical_when_disk_at_95(self):
        result = transform_telemetry(make_telemetry(disk=95.0))
        assert result['health_status'] == 'CRITICAL'

    def test_degraded_when_cpu_at_85(self):
        result = transform_telemetry(make_telemetry(cpu=85.0))
        assert result['health_status'] == 'DEGRADED'

    def test_degraded_when_memory_at_90(self):
        result = transform_telemetry(make_telemetry(memory=90.0))
        assert result['health_status'] == 'DEGRADED'

    def test_degraded_when_disk_at_90(self):
        result = transform_telemetry(make_telemetry(disk=90.0))
        assert result['health_status'] == 'DEGRADED'


class TestTransformUptime:
    def test_returns_required_fields(self):
        result = transform_uptime(make_uptime())
        for field in ['total_targets', 'up', 'down', 'avg_response_time_ms', 'overall_health', 'uptime_percent', 'targets']:
            assert field in result, f"Missing field: {field}"

    def test_uptime_percent_calculation_is_correct(self):
        result = transform_uptime(make_uptime(total=5, up=4))
        assert result['uptime_percent'] == 80.0

    def test_uptime_percent_100_when_all_up(self):
        result = transform_uptime(make_uptime(total=5, up=5, down=0))
        assert result['uptime_percent'] == 100.0

    def test_uptime_percent_0_when_all_down(self):
        result = transform_uptime(make_uptime(total=5, up=0, down=5))
        assert result['uptime_percent'] == 0.0

    def test_targets_list_is_built_correctly(self):
        result = transform_uptime(make_uptime())
        assert len(result['targets']) == 2

    def test_overall_health_is_preserved(self):
        result = transform_uptime(make_uptime(health='DEGRADED'))
        assert result['overall_health'] == 'DEGRADED'


class TestTransformIncidents:
    def test_empty_incidents_returns_zeros(self):
        result = transform_incidents(make_incidents([]))
        assert result['total_incidents'] == 0
        assert result['open'] == 0
        assert result['closed'] == 0
        assert result['critical_open'] == 0

    def test_total_incidents_count_is_correct(self):
        incidents = [
            {'severity': 'HIGH', 'status': 'OPEN'},
            {'severity': 'CRITICAL', 'status': 'OPEN'},
            {'severity': 'MEDIUM', 'status': 'CLOSED'},
        ]
        result = transform_incidents(make_incidents(incidents))
        assert result['total_incidents'] == 3

    def test_open_count_is_correct(self):
        incidents = [
            {'severity': 'HIGH', 'status': 'OPEN'},
            {'severity': 'MEDIUM', 'status': 'CLOSED'},
        ]
        result = transform_incidents(make_incidents(incidents))
        assert result['open'] == 1

    def test_closed_count_is_correct(self):
        incidents = [
            {'severity': 'HIGH', 'status': 'OPEN'},
            {'severity': 'MEDIUM', 'status': 'CLOSED'},
            {'severity': 'LOW', 'status': 'CLOSED'},
        ]
        result = transform_incidents(make_incidents(incidents))
        assert result['closed'] == 2

    def test_critical_open_count_is_correct(self):
        incidents = [
            {'severity': 'CRITICAL', 'status': 'OPEN'},
            {'severity': 'CRITICAL', 'status': 'CLOSED'},
            {'severity': 'HIGH', 'status': 'OPEN'},
        ]
        result = transform_incidents(make_incidents(incidents))
        assert result['critical_open'] == 1

    def test_severity_counts_are_correct(self):
        incidents = [
            {'severity': 'CRITICAL', 'status': 'OPEN'},
            {'severity': 'HIGH', 'status': 'OPEN'},
            {'severity': 'HIGH', 'status': 'OPEN'},
            {'severity': 'MEDIUM', 'status': 'CLOSED'},
        ]
        result = transform_incidents(make_incidents(incidents))
        assert result['severity_counts']['CRITICAL'] == 1
        assert result['severity_counts']['HIGH'] == 2
        assert result['severity_counts']['MEDIUM'] == 1


class TestTransformLogIntelligence:
    def test_returns_required_fields(self):
        result = transform_log_intelligence(make_log_intelligence())
        for field in ['file', 'health_status', 'total_entries', 'error_rate', 'warning_rate']:
            assert field in result, f"Missing field: {field}"

    def test_health_status_is_correct(self):
        result = transform_log_intelligence(make_log_intelligence(health='CRITICAL'))
        assert result['health_status'] == 'CRITICAL'

    def test_error_rate_is_correct(self):
        result = transform_log_intelligence(make_log_intelligence(error_rate=2.5))
        assert result['error_rate'] == 2.5

    def test_empty_summary_returns_empty_dict(self):
        result = transform_log_intelligence({'summary': []})
        assert result == {}