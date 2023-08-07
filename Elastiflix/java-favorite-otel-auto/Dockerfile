# Start with a base image containing Java runtime
FROM maven:3.8.2-openjdk-17-slim as build

# Make port 8080 available to the world outside this container
EXPOSE 5000

# Change to the app directory
WORKDIR /usr/src/app

# Copy the local code to the container
COPY . .

# Build the application
RUN mvn clean install

USER root
RUN apt-get update && apt-get install -y zip curl
RUN mkdir /otel
RUN curl -L -o /otel/opentelemetry-javaagent.jar https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/download/v1.28.0/opentelemetry-javaagent.jar

COPY start.sh /start.sh
RUN chmod +x /start.sh

ENTRYPOINT ["/start.sh"]
