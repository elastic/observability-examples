FROM python:3.9-slim as base

# get packages
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app

COPY . .
ENV FLASK_APP=helloworld
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080
EXPOSE 8080
ENTRYPOINT [ "flask", "run" ]
