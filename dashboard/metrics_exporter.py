import time
import psutil
import boto3
import requests
from prometheus_client import start_http_server, Gauge

# --- Prometheus Gauges ---
cpu_gauge = Gauge('cloudops_cpu_percent', 'CPU usage percent')
memory_gauge = Gauge('cloudops_memory_percent', 'Memory usage percent')
disk_gauge = Gauge('cloudops_disk_percent', 'Disk usage percent')
uptime_gauge = Gauge('cloudops_uptime_percent', 'Uptime percentage across targets')
avg_response_gauge = Gauge('cloudops_avg_response_time_ms', 'Average response time in ms')
open_incidents_gauge = Gauge('cloudops_open_incidents', 'Number of open incidents')
critical_incidents_gauge = Gauge('cloudops_critical_incidents', 'Number of critical open incidents')
log_error_gauge = Gauge('cloudops_log_error_rate', 'Log error rate percent')

# --- Uptime Targets ---
UPTIME_TARGETS = [
    'https://www.google.com',
    'https://www.github.com',
    'https://httpbin.org/get',
    'https://console.aws.amazon.com',
    'https://httpbin.org/status/500',
]

# --- CloudWatch Alarm Names ---
CRITICAL_ALARMS = [
    'cloudops-cpu-critical',
    'cloudops-memory-critical',
    'cloudops-disk-critical',
]

# --- Log file to scan ---
LOG_FILE = 'logs/dashboard.log'


def collect_system_metrics():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return cpu, memory, disk


def collect_uptime_metrics():
    results = []
    for url in UPTIME_TARGETS:
        try:
            r = requests.get(url, timeout=5)
            results.append({
                'status': 'UP' if r.status_code < 500 else 'DOWN',
                'response_time_ms': r.elapsed.total_seconds() * 1000
            })
        except Exception:
            results.append({'status': 'DOWN', 'response_time_ms': None})

    up = sum(1 for r in results if r['status'] == 'UP')
    times = [r['response_time_ms'] for r in results if r['response_time_ms'] is not None]
    uptime_pct = round(up / len(results) * 100, 2)
    avg_response = round(sum(times) / len(times), 2) if times else 0.0
    return uptime_pct, avg_response


def collect_incident_metrics():
    try:
        client = boto3.client('cloudwatch', region_name='us-east-2')
        response = client.describe_alarms(
            AlarmNames=CRITICAL_ALARMS,
            StateValue='ALARM'
        )
        alarms_firing = response['MetricAlarms']
        open_count = len(alarms_firing)
        critical_count = len(alarms_firing)
        return open_count, critical_count
    except Exception as e:
        print(f"    ⚠️  CloudWatch alarm query failed: {e}")
        return 0, 0


def collect_log_error_rate():
    try:
        with open(LOG_FILE, 'r') as f:
            lines = f.readlines()
        if not lines:
            return 0.0
        error_lines = sum(1 for l in lines if 'ERROR' in l)
        return round(error_lines / len(lines) * 100, 4)
    except Exception:
        return 0.0


def collect_and_expose():
    print("  Collecting live metrics...")

    cpu, memory, disk = collect_system_metrics()
    cpu_gauge.set(cpu)
    memory_gauge.set(memory)
    disk_gauge.set(disk)
    print(f"    ✅ System — CPU: {cpu}% | Memory: {memory}% | Disk: {disk}%")

    uptime_pct, avg_response = collect_uptime_metrics()
    uptime_gauge.set(uptime_pct)
    avg_response_gauge.set(avg_response)
    print(f"    ✅ Uptime — {uptime_pct}% | Avg Response: {avg_response}ms")

    open_inc, critical_inc = collect_incident_metrics()
    open_incidents_gauge.set(open_inc)
    critical_incidents_gauge.set(critical_inc)
    print(f"    ✅ Incidents — Open: {open_inc} | Critical: {critical_inc}")

    error_rate = collect_log_error_rate()
    log_error_gauge.set(error_rate)
    print(f"    ✅ Log Error Rate — {error_rate}%")


if __name__ == "__main__":
    print("=" * 50)
    print("  CloudOps Metrics Exporter — Live Mode")
    print("  Serving on http://localhost:8000/metrics")
    print("=" * 50)
    start_http_server(8000)
    while True:
        collect_and_expose()
        print()
        time.sleep(15)