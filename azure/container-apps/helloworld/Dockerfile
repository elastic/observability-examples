FROM ${ARCH}mcr.microsoft.com/dotnet/aspnet:7.0. AS base
WORKDIR /app

FROM mcr.microsoft.com/dotnet/sdk:8.0-preview AS build
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

ENTRYPOINT ["dotnet", "helloworld.dll"]
