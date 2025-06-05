# Use glibc-based image with pre-compiled wheels for psutil
FROM python:3.13-slim

RUN python -m pip install --upgrade pip
RUN pip install \
    # litellm proxy requirements
    litellm[proxy]~=1.72.1 \
    opentelemetry-exporter-otlp-proto-http~=1.34.0 \
    # TODO: required until https://github.com/BerriAI/litellm/issues/9901
    opentelemetry-exporter-otlp-proto-grpc~=1.34.0

COPY config.yaml /

EXPOSE 4000

CMD [ "litellm", "-c", "config.yaml", "--detailed_debug" ]
