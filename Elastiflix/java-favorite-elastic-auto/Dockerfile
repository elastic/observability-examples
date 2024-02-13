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

COPY start.sh /start.sh
RUN chmod +x /start.sh

ARG AGENT_VERSION=1.46.0
USER root
RUN apt-get update && apt-get install -y zip curl
RUN mkdir /elastic_apm_agent

RUN curl -L -o /elastic_apm_agent/elastic-apm-agent.jar https://repo1.maven.org/maven2/co/elastic/apm/elastic-apm-agent/${AGENT_VERSION}/elastic-apm-agent-${AGENT_VERSION}.jar

ENTRYPOINT ["/start.sh"]
