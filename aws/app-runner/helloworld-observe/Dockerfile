FROM python:3.9-slim as base

# get packages
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app

# install opentelemetry packages
RUN pip install opentelemetry-distro opentelemetry-exporter-otlp
RUN opentelemetry-bootstrap -a install

ENV OTEL_EXPORTER_OTLP_ENDPOINT='<ELASTIC_APM_SERVER_URL>'
ENV OTEL_EXPORTER_OTLP_HEADERS='Authorization=Bearer%20<ELASTIC_APM_SECRET_TOKEN>'
ENV OTEL_LOG_LEVEL=info
ENV OTEL_METRICS_EXPORTER=otlp
ENV OTEL_RESOURCE_ATTRIBUTES=service.version=1.0,deployment.environment=production
ENV OTEL_SERVICE_NAME=helloworld
ENV OTEL_TRACES_EXPORTER=otlp

COPY . .
ENV FLASK_APP=helloworld
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080
EXPOSE 8080
ENTRYPOINT [ "opentelemetry-instrument", "flask", "run" ]
