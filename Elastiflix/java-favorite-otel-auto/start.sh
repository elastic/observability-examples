#!/bin/sh
java -javaagent:/otel/opentelemetry-javaagent.jar \
-jar /usr/src/app/target/favorite-0.0.1-SNAPSHOT.jar --server.port=5000