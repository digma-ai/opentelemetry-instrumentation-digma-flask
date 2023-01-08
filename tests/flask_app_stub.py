from flask import Flask
from opentelemetry import trace

def configure_app_routes(app: Flask):

    @app.route('/span')
    def check_span_exists():
        span = trace.get_current_span();
        return span.name

    @app.route('/span_attribute/<attribute>')
    def check_span_attribute_value(attribute):
        span = trace.get_current_span()
        return span.attributes[attribute]