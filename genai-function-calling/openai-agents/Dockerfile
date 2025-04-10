# Use glibc-based image with pre-compiled wheels for psutil
FROM python:3.12-slim

RUN --mount=type=cache,target=/root/.cache/pip python -m pip install --upgrade pip

COPY requirements.txt /tmp
RUN --mount=type=cache,target=/root/.cache/pip pip install -r /tmp/requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip edot-bootstrap --action=install

COPY main.py /
COPY mcp_server.py /

ENTRYPOINT [ "opentelemetry-instrument", "python", "main.py" ]
