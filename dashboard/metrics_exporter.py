from prometheus_client import start_http_server, Gauge
import time
from dashboard.aggregator import aggregate_all
from dashboard.transformer import transform_all

# Define metrics
cpu_percent = Gauge('cloudops_cpu_percent', 'CPU usage percent')
memory_percent = Gauge('cloudops_memory_percent', 'Memory usage percent')
disk_percent = Gauge('cloudops_disk_percent', 'Disk usage percent')
uptime_percent = Gauge('cloudops_uptime_percent', 'Uptime percentage across targets')
avg_response_time = Gauge('cloudops_avg_response_time_ms', 'Average response time in ms')
open_incidents = Gauge('cloudops_open_incidents', 'Number of open incidents')
critical_incidents = Gauge('cloudops_critical_incidents', 'Number of critical open incidents')
log_error_rate = Gauge('cloudops_log_error_rate', 'Log error rate percent')


def collect_and_expose():
    aggregated = aggregate_all()
    transformed = transform_all(aggregated)

    cpu_percent.set(transformed['telemetry']['cpu_percent'])
    memory_percent.set(transformed['telemetry']['memory_percent'])
    disk_percent.set(transformed['telemetry']['disk_percent'])
    uptime_percent.set(transformed['uptime']['uptime_percent'])
    avg_response_time.set(transformed['uptime']['avg_response_time_ms'])
    open_incidents.set(transformed['incidents']['open'])
    critical_incidents.set(transformed['incidents']['critical_open'])
    log_error_rate.set(transformed['log_intelligence']['error_rate'])


if __name__ == "__main__":
    print("Starting CloudOps metrics exporter on port 8000...")
    start_http_server(8000)
    while True:
        collect_and_expose()
        time.sleep(15)