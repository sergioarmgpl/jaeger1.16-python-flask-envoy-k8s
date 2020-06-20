from opentelemetry import metrics
from opentelemetry.ext.prometheus import PrometheusMetricsExporter
from opentelemetry.sdk.metrics import Counter, MeterProvider
from prometheus_client import start_http_server

# Start Prometheus client
start_http_server(port=5555, addr="0.0.0.0")

# Meter is responsible for creating and recording metrics
metrics.set_meter_provider(MeterProvider())
meter = metrics.get_meter(__name__)
# exporter to export metrics to Prometheus
prefix = "MyAppPrefix"
exporter = PrometheusMetricsExporter(prefix)
# Starts the collect/export pipeline for metrics
metrics.get_meter_provider().start_pipeline(meter, exporter, 5)

counter = meter.create_metric(
    "requests",
    "number of requests",
    "requests",
    int,
    Counter,
    ("environment",),
)

# Labels are used to identify key-values that are associated with a specific
# metric that you want to record. These are useful for pre-aggregation and can
# be used to store custom dimensions pertaining to a metric
labels = {"environment": "staging"}

counter.add(25, labels)
#input("Press any key to exit...")
