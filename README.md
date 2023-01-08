# opentelemetry-instrumentation-digma-flask
Instrumentation package for the Flask platform adding code linkage to traces


## Installing the package
```bash
pip install opentelemetry-instrumentation-digma-flask
```
Or add it to your requirements/poetry file.

## Instrumenting your Flask project

### Enable OpenTelemetry in your project
First, configure OpenTelemetry in your project. See the [Digma instrumentation](https://github.com/digma-ai/opentelemetry-instrumentation-digma) repo for quick instructions on getting that done, whether you're already using OTEL or not.

Make sure you've instrumented your Flask application using the standard Pypi package.
1. Install the package:
``` pip install opentelemetry-instrumentation-flask ```
2. Instrument the Flask app by adding the following to your app setup: 
```python 
FlaskInstrumentor.instrument_app(app) 
```

More info can be found in the [official package documentation](https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/flask/flask.html). 

### Enable the Digma OpenTelemetry instrumentation

After the call to ```FlaskInstrumentor.instrument``` to enable OTEL, also add the following:

```python 
DigmaFlaskInstrumentor().instrument_app(app)
```

### Check out some sample projects

Coming soon!