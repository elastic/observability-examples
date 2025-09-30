# Use glibc-based image with pre-compiled wheels for psutil
FROM python:3.13-slim

# TODO: temporary until elastic-opentelemetry release with https://github.com/elastic/elastic-otel-python-instrumentations/pull/90
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip python -m pip install --upgrade pip

COPY requirements.txt /tmp
RUN --mount=type=cache,target=/root/.cache/pip pip install -r /tmp/requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip edot-bootstrap --action=install

COPY *.py /

ENTRYPOINT [ "opentelemetry-instrument", "python", "main.py" ]
