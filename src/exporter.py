"""Application exporter"""

import os
import time
from prometheus_client import start_http_server, Gauge


from pixie import PixieMetrics

ns_per_ms = 1000 * 1000
ns_per_s = 1000 * ns_per_ms

class AppMetrics:
    """
    Representation of Prometheus metrics and loop to fetch and transform
    application metrics into Prometheus metrics.
    """

    def __init__(self, polling_interval_seconds=30):
        self.polling_interval_seconds = polling_interval_seconds

        # Prometheus metrics to collect
        self.request_throughput = Gauge("sli_service_request_throughput", "Requests troughput in seconds", ["service"])
        self.error_rate = Gauge("sli_service_error_rate", "Error rate %", ["service"])
        self.latency_p50 = Gauge("sli_service_latency_p50", "Latency p50 in ns", ["service"])
        self.latency_p90 = Gauge("sli_service_latency_p90", "Latency p90 in ns", ["service"])
        self.latency_p99 = Gauge("sli_service_latency_p99", "Latency p99 in ns", ["service"])

        # Pixie client
        self.pixie = PixieMetrics()

    def run_metrics_loop(self):
        """Metrics fetching loop"""

        while True:
            self.fetch()
            time.sleep(self.polling_interval_seconds)

    def fetch(self):
        """
        Get metrics from Pixie and refresh Prometheus metrics with
        new values.
        """

        metrics = self.pixie.get_metrics()

        for service in metrics:
            self.request_throughput.labels(service["service"]).set(round(service["request_throughput"]*ns_per_s,5))
            self.error_rate.labels(service["service"]).set(round(service["error_rate"],2))
            self.latency_p50.labels(service["service"]).set(round(service["latency_p50"],2))
            self.latency_p90.labels(service["service"]).set(round(service["latency_p90"],2))
            self.latency_p99.labels(service["service"]).set(round(service["latency_p99"],2))

def main():
    """Main entry point"""

    polling_interval_seconds = int(os.getenv("POLLING_INTERVAL_SECONDS", "30"))
    exporter_port = int(os.getenv("EXPORTER_PORT", "9877"))

    app_metrics = AppMetrics(
        polling_interval_seconds=polling_interval_seconds
    )
    start_http_server(exporter_port)
    app_metrics.run_metrics_loop()

if __name__ == "__main__":
    main()