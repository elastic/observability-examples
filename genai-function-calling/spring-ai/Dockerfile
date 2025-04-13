FROM eclipse-temurin:21-jdk-alpine AS build

WORKDIR /build

# Install dependencies (verify resolves more than dependency:go-offline)
COPY mvnw ./
COPY .mvn ./.mvn
COPY pom.xml ./
RUN ./mvnw verify -DskipTests

# Copy source code and build the application
COPY src ./src
RUN ./mvnw package

FROM eclipse-temurin:21-jre-alpine

COPY --from=build /build/target/genai-function-calling-*.jar /genai-function-calling.jar
COPY --from=build /build/target/elastic-otel-javaagent.jar /elastic-otel-javaagent.jar

ENTRYPOINT ["java", "-javaagent:/elastic-otel-javaagent.jar", "-cp", "./genai-function-calling.jar", "org.springframework.boot.loader.launch.PropertiesLauncher"]
