from opentelemetry.instrumentation.flask import FlaskInstrumentor

from opentelemetry import trace
import pytest
from flask import Flask
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.digma import DigmaConfiguration
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace import TracerProvider
from src.opentelemetry.instrumentation.digma.flask import DigmaFlaskInstrumentor
from opentelemetry.semconv.trace import SpanAttributes

from tests.flask_app_stub import configure_app_routes


@pytest.fixture()
def app():
    app = Flask(__name__)
    stub = configure_app_routes(app)
    app.config.update({
        "TESTING": True,
    })
    resource = Resource.create(attributes={SERVICE_NAME: 'flask_service'})
    exporter = OTLPSpanExporter(endpoint="http://localhost:5050", insecure=True)
    resource = DigmaConfiguration().trace_this_package() \
        .set_environment("CI").resource.merge(resource)
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    FlaskInstrumentor().instrument_app(app)
    DigmaFlaskInstrumentor.instrument_app(app)
    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()

def test_request_example(client):
    response = client.get("/span")
    assert response.text == "/span";

def test_code_location_is_set_on_span_example(client):
    response = client.get(f'/span_attribute/{SpanAttributes.CODE_FILEPATH}')
    assert response.text == configure_app_routes.__code__.co_filename

def test_function_name_is_set_on_span_example(client):
    response = client.get(f'/span_attribute/{SpanAttributes.CODE_FUNCTION}')
    assert response.text == 'configure_app_routes.<locals>.check_span_attribute_value'
