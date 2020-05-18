#tracing and metrics
import flask
import requests

import opentelemetry.ext.requests
from opentelemetry import trace
from opentelemetry.ext import jaeger
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.sdk.trace.export import SimpleExportSpanProcessor
from opentelemetry.ext.flask import FlaskInstrumentor
#metrics libraries
import sys
import time
from opentelemetry import metrics
from opentelemetry.sdk.metrics import Counter, MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricsExporter
from opentelemetry.sdk.metrics.export.controller import PushController

jaeger_exporter = jaeger.JaegerSpanExporter(
    service_name="my-traced-service", agent_host_name="simplest-agent.observability.svc.cluster.local", agent_port=6831
)

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    SimpleExportSpanProcessor(jaeger_exporter)
)

app = flask.Flask(__name__)
FlaskInstrumentor().instrument_app(app)
opentelemetry.ext.requests.RequestsInstrumentor().instrument()

@app.route("/")
def hello():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("step1"):

        #adding metrics
        metrics.set_meter_provider(MeterProvider())
        meter = metrics.get_meter(__name__, True)
        exporter = ConsoleMetricsExporter()
        controller = PushController(meter, exporter, 5)
        #adding label
        staging_labels = {"environment": "staging"}

        requests_counter = meter.create_metric(
            name="requests",
            description="number of requests",
            unit="1",
            value_type=int,
            metric_type=Counter,
            label_keys=("environment",),
        )
        requests_counter.add(25, staging_labels)
    
        with tracer.start_as_current_span("step2"):
            requests.get("http://www.example.com")
    return "jaeger"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
