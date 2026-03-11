import pytest
from dashboard.summary import generate_summary


def make_transformed(
    telemetry_health='HEALTHY',
    uptime_health='HEALTHY',
    log_health='HEALTHY',
    critical_open=0,
    open_incidents=0,
    total_incidents=0,
    severity_counts=None,
    cpu=10.0,
    memory=50.0,
    disk=30.0,
    uptime_percent=100.0,
    avg_response=200.0,
    error_rate=0.1
):
    """Helper — build a fully transformed dashboard payload with controlled values."""
    return {
        'telemetry': {
            'health_status': telemetry_health,
            'cpu_percent': cpu,
            'memory_percent': memory,
            'disk_percent': disk,
            'hostname': 'test-server',
            'environment': 'production'
        },
        'uptime': {
            'overall_health': uptime_health,
            'uptime_percent': uptime_percent,
            'avg_response_time_ms': avg_response,
            'total_targets': 5,
            'up': 5,
            'down': 0,
            'targets': []
        },
        'incidents': {
            'total_incidents': total_incidents,
            'open': open_incidents,
            'closed': 0,
            'critical_open': critical_open,
            'severity_counts': severity_counts or {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        },
        'log_intelligence': {
            'health_status': log_health,
            'error_rate': error_rate,
            'file': 'test.log',
            'total_entries': 1000,
            'warning_rate': 0.0
        }
    }


class TestOverallHealthScoring:
    def test_healthy_when_all_components_healthy(self):
        result = generate_summary(make_transformed())
        assert result['overall_health'] == 'HEALTHY'

    def test_degraded_when_telemetry_degraded(self):
        result = generate_summary(make_transformed(telemetry_health='DEGRADED'))
        assert result['overall_health'] == 'DEGRADED'

    def test_degraded_when_uptime_degraded(self):
        result = generate_summary(make_transformed(uptime_health='DEGRADED'))
        assert result['overall_health'] == 'DEGRADED'

    def test_degraded_when_log_degraded(self):
        result = generate_summary(make_transformed(log_health='DEGRADED'))
        assert result['overall_health'] == 'DEGRADED'

    def test_critical_when_telemetry_critical(self):
        result = generate_summary(make_transformed(telemetry_health='CRITICAL'))
        assert result['overall_health'] == 'CRITICAL'

    def test_critical_when_uptime_critical(self):
        result = generate_summary(make_transformed(uptime_health='CRITICAL'))
        assert result['overall_health'] == 'CRITICAL'

    def test_critical_when_log_critical(self):
        result = generate_summary(make_transformed(log_health='CRITICAL'))
        assert result['overall_health'] == 'CRITICAL'

    def test_critical_when_open_critical_incidents_exist(self):
        result = generate_summary(make_transformed(critical_open=1))
        assert result['overall_health'] == 'CRITICAL'


class TestCriticalTakesPriorityOverDegraded:
    def test_critical_beats_degraded_components(self):
        result = generate_summary(make_transformed(
            telemetry_health='DEGRADED',
            uptime_health='DEGRADED',
            critical_open=1
        ))
        assert result['overall_health'] == 'CRITICAL'

    def test_critical_component_beats_degraded(self):
        result = generate_summary(make_transformed(
            telemetry_health='CRITICAL',
            uptime_health='DEGRADED'
        ))
        assert result['overall_health'] == 'CRITICAL'


class TestSummaryStructure:
    def test_summary_contains_required_fields(self):
        result = generate_summary(make_transformed())
        for field in ['generated_at', 'overall_health', 'ecosystem', 'metrics', 'incidents']:
            assert field in result, f"Missing field: {field}"

    def test_ecosystem_contains_component_health_fields(self):
        result = generate_summary(make_transformed())
        ecosystem = result['ecosystem']
        for field in ['telemetry_health', 'uptime_health', 'log_health', 'open_incidents', 'critical_incidents']:
            assert field in ecosystem, f"Missing ecosystem field: {field}"

    def test_metrics_contains_key_metrics(self):
        result = generate_summary(make_transformed())
        metrics = result['metrics']
        for field in ['cpu_percent', 'memory_percent', 'disk_percent', 'uptime_percent', 'avg_response_time_ms', 'log_error_rate']:
            assert field in metrics, f"Missing metrics field: {field}"

    def test_incidents_section_is_correct(self):
        result = generate_summary(make_transformed(
            total_incidents=3,
            open_incidents=2,
            critical_open=1
        ))
        assert result['incidents']['total'] == 3
        assert result['incidents']['open'] == 2

    def test_generated_at_is_present(self):
        result = generate_summary(make_transformed())
        assert result['generated_at'] is not None


class TestMetricValuesPassThrough:
    def test_cpu_percent_is_correct(self):
        result = generate_summary(make_transformed(cpu=42.5))
        assert result['metrics']['cpu_percent'] == 42.5

    def test_memory_percent_is_correct(self):
        result = generate_summary(make_transformed(memory=78.0))
        assert result['metrics']['memory_percent'] == 78.0

    def test_uptime_percent_is_correct(self):
        result = generate_summary(make_transformed(uptime_percent=80.0))
        assert result['metrics']['uptime_percent'] == 80.0

    def test_error_rate_is_correct(self):
        result = generate_summary(make_transformed(error_rate=2.5))
        assert result['metrics']['log_error_rate'] == 2.5


class TestEcosystemHealthReflectsComponents:
    def test_telemetry_health_reflects_input(self):
        result = generate_summary(make_transformed(telemetry_health='DEGRADED'))
        assert result['ecosystem']['telemetry_health'] == 'DEGRADED'

    def test_uptime_health_reflects_input(self):
        result = generate_summary(make_transformed(uptime_health='CRITICAL'))
        assert result['ecosystem']['uptime_health'] == 'CRITICAL'

    def test_open_incidents_count_reflects_input(self):
        result = generate_summary(make_transformed(open_incidents=5))
        assert result['ecosystem']['open_incidents'] == 5

    def test_critical_incidents_count_reflects_input(self):
        result = generate_summary(make_transformed(critical_open=3))
        assert result['ecosystem']['critical_incidents'] == 3