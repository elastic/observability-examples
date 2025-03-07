FROM eclipse-temurin:21-jdk-alpine AS build

WORKDIR /build

# Copy the local code to the container
COPY mvnw pom.xml ./
COPY src ./src
COPY .mvn ./.mvn

RUN ./mvnw package

FROM eclipse-temurin:21-jre-alpine

COPY --from=build /build/target/genai-function-calling-*.jar /genai-function-calling.jar
COPY --from=build /build/target/elastic-otel-javaagent.jar /elastic-otel-javaagent.jar

ENTRYPOINT ["java", "-javaagent:/elastic-otel-javaagent.jar", "-cp", "./genai-function-calling.jar", "org.springframework.boot.loader.launch.PropertiesLauncher"]
