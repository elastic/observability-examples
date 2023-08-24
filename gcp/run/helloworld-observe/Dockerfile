FROM node:18-slim
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install --only=production
COPY . ./
ENV OTEL_EXPORTER_OTLP_ENDPOINT='ELASTIC_APM_SERVER_URL'
ENV OTEL_EXPORTER_OTLP_HEADERS='Authorization=Bearer ELASTIC_APM_SECRET_TOKEN'
ENV OTEL_LOG_LEVEL=info
ENV OTEL_METRICS_EXPORTER=otlp
ENV OTEL_RESOURCE_ATTRIBUTES=service.version=1.0,deployment.environment=production
ENV OTEL_SERVICE_NAME=helloworld
ENV OTEL_TRACES_EXPORTER=otlp
RUN npm install --save @opentelemetry/api
RUN npm install --save @opentelemetry/auto-instrumentations-node
CMD ["node", "--require", "@opentelemetry/auto-instrumentations-node/register", "index.js"]
