#!/bin/sh

agent_path=''
case "${OTEL_DISTRIBUTION:-otel}" in
  elastic)
    agent_path='/elastic/elastic-otel-javaagent.jar'
    ;;
  otel)
    agent_path='/otel/opentelemetry-javaagent.jar'
    ;;
  *)
    echo "unknown otel distribution: ${OTEL_DISTRIBUTION}"
    exit 1
  ;;
esac

java -javaagent:${agent_path} \
-jar /usr/src/app/target/favorite-0.0.1-SNAPSHOT.jar --server.port=5000