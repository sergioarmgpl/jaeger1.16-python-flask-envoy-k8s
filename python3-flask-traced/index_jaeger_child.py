#tracing and metrics
import time
import flask
import requests
from flask import request

import opentelemetry.ext.requests
from opentelemetry import trace
from opentelemetry.ext import jaeger
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.sdk.trace.export import SimpleExportSpanProcessor
from opentelemetry.ext.flask import FlaskInstrumentor

from opentelemetry.sdk.trace.export import BatchExportSpanProcessor
from opentelemetry.ext.wsgi import OpenTelemetryMiddleware


'''
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
'''

#--------------------------------------------------------------
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# create a JaegerSpanExporter
jaeger_exporter = jaeger.JaegerSpanExporter(
    service_name="my-traced-service", 
    agent_host_name="simplest-agent.observability.svc.cluster.local", 
    agent_port=6831,
    # optional: configure also collector
    # collector_host_name='localhost',
    # collector_port=14268,
    # collector_endpoint='/api/traces?format=jaeger.thrift',
    # username=xxxx, # optional
    # password=xxxx, # optional    
)

# Create a BatchExportSpanProcessor and add the exporter to it
span_processor = BatchExportSpanProcessor(jaeger_exporter)

# add to the tracer
trace.get_tracer_provider().add_span_processor(span_processor)

app = flask.Flask(__name__)
app.wsgi_app = OpenTelemetryMiddleware(app.wsgi_app)#wsgi

FlaskInstrumentor().instrument_app(app)
opentelemetry.ext.requests.RequestsInstrumentor().instrument()
#--------------------------------------------------------------

@app.route("/example4")
def span_attributes():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("step1") as span1:
        span1.set_attribute("attribute1","value1")
        with tracer.start_as_current_span("step2") as span2:
            r = requests.get("http://jaeger-app-srv-2:5555/example1")
            span2.set_attribute("attribute1",str(request.headers))
            span2.set_attribute("response",str(r))
    return "distribute context 1"

@app.route("/example6")
def span_end_road():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("step1") as span1:
        span.add_event("end of the road",{"error": "no no no"})
    return "distribute context 2"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
