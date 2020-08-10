#tracing simple
import flask
import requests

import opentelemetry.ext.requests
from opentelemetry import trace
from opentelemetry.ext import jaeger
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.sdk.trace.export import SimpleExportSpanProcessor
from opentelemetry.ext.flask import FlaskInstrumentor

jaeger_exporter = jaeger.JaegerSpanExporter(
    service_name="my-helloworld-service", agent_host_name="simplest-agent.observability.svc.cluster.local", agent_port=6831
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
    with tracer.start_as_current_span("example-request"):
        requests.get("http://www.example.com")
    return "hello"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
