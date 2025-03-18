# Use glibc-based image with pre-compiled wheels for psutil
FROM python:3.12-slim

# TODO: temporary until openai-agents 0.0.5
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip python -m pip install --upgrade pip

COPY requirements.txt /tmp
RUN --mount=type=cache,target=/root/.cache/pip pip install -r /tmp/requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip edot-bootstrap --action=install
# TODO(EDOT): remove when > v0.6.1
RUN pip uninstall -y elastic-opentelemetry-instrumentation-openai \
    && apt-get update \
    && apt-get install -y --no-install-recommends git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip uninstall -y elastic-opentelemetry-instrumentation-openai \
    && pip install 'elastic-opentelemetry-instrumentation-openai @ git+https://github.com/elastic/elastic-otel-python-instrumentations.git@main#subdirectory=instrumentation/elastic-opentelemetry-instrumentation-openai'

COPY main.py /

CMD [ "python", "main.py" ]
