#tracing and metrics
import time
import flask
import requests

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



@app.route("/example1")
def span_attributes():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("step1") as span1:
        span1.set_attribute("attribute1","value1")
        with tracer.start_as_current_span("step2") as span2:
            span2.set_attribute("attribute2","value1")
    return "span and attributes"

@app.route("/example3")
def span_attributes_slow():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("step1") as span1:
        time.sleep(1)
        span1.set_attribute("attribute1","value1")
        time.sleep(1)
        with tracer.start_as_current_span("step2") as span2:
            time.sleep(1)
            span2.set_attribute("attribute2","value1")
            time.sleep(1)
    return "span and attributes slow version"

@app.route("/example2")
def span_errors():
    try:
        n = 100/0
    except Exception as e:
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("step1"):
            with tracer.start_as_current_span("step2") as span:
                span.add_event("error occured",{"error": str(e)})
        return "error",500

@app.route("/example5")
def span_call_child():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("step1") as span1:
        requests.get("http://jaeger-app-2-srv-2:5555/example6")
    return "simple call"
   

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
