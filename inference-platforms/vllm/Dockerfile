# Pytorch doesn't build on Alpine, so we use Ubuntu instead.
# We can't use the official Pytorch image because it is x86 only.
FROM ubuntu:24.04

ARG VLLM_VERSION=v0.9.0.1

# Package pre-reqs copied from https://github.com/vllm-project/vllm/blob/main/docker/Dockerfile.arm
ENV CCACHE_DIR=/root/.cache/ccache
ENV CMAKE_CXX_COMPILER_LAUNCHER=ccache
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update -y \
    && apt-get install -y curl ccache git wget vim numactl gcc-12 g++-12 python3 python3-pip libtcmalloc-minimal4 libnuma-dev \
    && apt-get install -y ffmpeg libsm6 libxext6 libgl1 \
    && update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-12 10 --slave /usr/bin/g++ g++ /usr/bin/g++-12

# Install CMake 3.26+, required for installation
RUN --mount=type=cache,target=/var/cache/apt \
    wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | tee /usr/share/keyrings/kitware-archive-keyring.gpg >/dev/null \
    && . /etc/os-release \
    && echo "deb [signed-by=/usr/share/keyrings/kitware-archive-keyring.gpg] https://apt.kitware.com/ubuntu/ $UBUNTU_CODENAME main" | tee /etc/apt/sources.list.d/kitware.list >/dev/null \
    && apt-get install -y cmake

# Install Python and make a virtual environment
RUN apt-get install -y python3-dev python3-pip python3-setuptools python3-venv
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip

# tcmalloc provides better memory allocation efficiency, e.g., holding memory in caches to speed up access of commonly-used objects.
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install py-cpuinfo  # Use this to gather CPU info and optimize based on ARM Neoverse cores

# Set LD_PRELOAD for tcmalloc on ARM
ENV LD_PRELOAD="/usr/lib/aarch64-linux-gnu/libtcmalloc_minimal.so.4"

# Install from source
RUN git clone --depth 1 --single-branch --branch ${VLLM_VERSION} https://github.com/vllm-project/vllm.git
WORKDIR vllm

# Use old dependencies
# See https://github.com/vllm-project/vllm/blob/main/examples/online_serving/opentelemetry/README.md
RUN pip install \
      'opentelemetry-sdk>=1.26.0,<1.27.0' \
      'opentelemetry-api>=1.26.0,<1.27.0' \
      'opentelemetry-exporter-otlp>=1.26.0,<1.27.0' \
      'opentelemetry-semantic-conventions-ai>=0.4.1,<0.5.0'

# CPU-only in order to run on MacOS.
# See https://docs.vllm.ai/en/latest/getting_started/installation/cpu/index.html
RUN pip install "cmake>=3.26" wheel packaging ninja "setuptools-scm>=8" numpy
RUN pip install -v -r requirements/cpu.txt --extra-index-url https://download.pytorch.org/whl/cpu
RUN VLLM_TARGET_DEVICE=cpu python setup.py install

ENV CHAT_MODEL=Qwen/Qwen3-0.6B
ENV OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://localhost:11434/v1/traces

EXPOSE 8000

CMD vllm serve ${CHAT_MODEL} --max-model-len 4096 --enforce-eager --otlp-traces-endpoint=${OTEL_EXPORTER_OTLP_TRACES_ENDPOINT}
