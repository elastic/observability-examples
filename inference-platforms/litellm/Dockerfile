# Use glibc-based image with pre-compiled wheels for psutil
FROM python:3.13-slim

# Install build dependencies for fastuuid, needed by LiteLLM until
# https://github.com/fastuuid/fastuuid/pull/55 is released.
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip
RUN pip install \
    # litellm proxy requirements
    litellm[proxy]~=1.76.1 \
    opentelemetry-exporter-otlp-proto-http~=1.36.0 \
    # LiteLLM has a hard dependency on grpc even if it is not used.
    opentelemetry-exporter-otlp-proto-grpc~=1.36.0

COPY config.yaml /

EXPOSE 4000

CMD [ "litellm", "-c", "config.yaml", "--detailed_debug" ]
