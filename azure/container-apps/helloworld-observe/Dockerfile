FROM ${ARCH}mcr.microsoft.com/dotnet/aspnet:7.0. AS base
WORKDIR /app

FROM mcr.microsoft.com/dotnet/sdk:8.0-preview AS build
ARG TARGETPLATFORM

WORKDIR /src
COPY ["helloworld.csproj", "./"]
RUN dotnet restore "./helloworld.csproj"
COPY . .
WORKDIR "/src/."
RUN dotnet build "helloworld.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "helloworld.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
EXPOSE 3500
ENV ASPNETCORE_URLS=http://+:3500

ENV OTEL_EXPORTER_OTLP_ENDPOINT='ELASTIC_APM_SERVER_URL'
ENV OTEL_EXPORTER_OTLP_HEADERS='Authorization=Bearer ELASTIC_APM_SECRET_TOKEN'
ENV OTEL_LOG_LEVEL=info
ENV OTEL_METRICS_EXPORTER=otlp
ENV OTEL_RESOURCE_ATTRIBUTES=service.version=1.0,deployment.environment=production
ENV OTEL_SERVICE_NAME=helloworld
ENV OTEL_TRACES_EXPORTER=otlp

ENTRYPOINT ["dotnet", "helloworld.dll"]
