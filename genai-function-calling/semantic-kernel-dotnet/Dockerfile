ARG DOTNET_VERSION=9.0

FROM mcr.microsoft.com/dotnet/sdk:${DOTNET_VERSION}-alpine AS edot
ARG EDOT_VERSION=1.0.2
ARG EDOT_INSTALL=https://github.com/elastic/elastic-otel-dotnet/releases/download/${EDOT_VERSION}/elastic-dotnet-auto-install.sh
ENV OTEL_DOTNET_AUTO_HOME=/edot
WORKDIR /edot
RUN sh -c "$(curl -fsSL ${EDOT_INSTALL})"

FROM mcr.microsoft.com/dotnet/sdk:${DOTNET_VERSION}-alpine AS app
WORKDIR /app
COPY *.csproj ./
RUN dotnet restore
COPY . ./
RUN dotnet publish -c Release -p:AssemblyName=app -o out

FROM mcr.microsoft.com/dotnet/runtime:${DOTNET_VERSION}-alpine

# Copy EDOT from the build stage
ENV OTEL_DOTNET_AUTO_HOME=/edot
COPY --from=edot /edot /edot

# Copy the application dll from the build stage
WORKDIR /app
COPY --from=app /app/out .

ENTRYPOINT ["/edot/instrument.sh", "dotnet", "app.dll"]
