# Elastic Observability Hello World Demo App for Azure Container Apps

## Overview

This demo application has two parts: 
* helloworld - A simple C# web app
* helloworld-observe - A helloworld C# web app instrumented with minimal Elastic Observability

---

### Setup

1. Create an [Elastic Cloud Deployment](https://cloud.elastic.co)
   * In Elastic Cloud, select **Integrations** from the top-level menu. Then click the **APM** integrations tile.
   * Copy the Elastic APM **serverUrl** and save it for a later step.
   * Copy the Elastic APM **secretToken** and save it for a later step.

2. From the [Azure portal](https://portal.azure.com/), click the Cloud Shell icon **[>_]** at the top of the portal to open Cloud Shell.

3. In Azure Cloud Shell, define the environment variables that we’ll be using in the commands below.
```
RESOURCE_GROUP="helloworld-containerapps"
LOCATION="centralus"
ENVIRONMENT="env-helloworld-containerapps"
APP_NAME="elastic-helloworld"
```

4. Define a registry container name that is unique by running the following command.
```
ACR_NAME="helloworld"$RANDOM
```

5. Create an Azure resource group by running the following command.
```
az group create --name $RESOURCE_GROUP --location "$LOCATION"
```

6. Run the following command to create a registry container in Azure Container Registry (ACR).
```
az acr create --resource-group $RESOURCE_GROUP \
--name $ACR_NAME --sku Basic --admin-enable true
```

7. Register the Microsoft.OperationalInsights namespace as a provider by running the following command:
```
az provider register -n Microsoft.OperationalInsights --wait
```

### Deploy the app to Azure Container Apps
Clone this repo in Cloud Shell:
```
git clone https://github.com/elastic/observability-examples
```

---

#### helloworld
##### Build the app with Docker in Azure Cloud Shell and push the image to Azure Container Registry

1. In Cloud Shell, cd to the helloworld directory.
```
cd observability-examples/azure/container-apps/helloworld
```

2. Build the Hello World sample app:
```
az acr build --registry $ACR_NAME --image $APP_NAME .
```
##### Deploy the app to Azure Container Apps

1. Run the following command to create a Container App environment for deploying your app into.
```
az containerapp env create --name $ENVIRONMENT \
--resource-group $RESOURCE_GROUP --location "$LOCATION"
```

2. Create a new Container App by deploying the Hello World app’s image to Container Apps, using the following command.
```
az containerapp create \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $ENVIRONMENT \
  --image $ACR_NAME.azurecr.io/$APP_NAME \
  --target-port 3500 \
  --ingress 'external' \
  --registry-server $ACR_NAME.azurecr.io \
  --query properties.configuration.ingress.fqdn
```
This command will output the deployed Hello World app's fully qualified domain name (FQDN). Copy and paste the FQDN into a browser to see the running Hello World app.

---

#### helloworld-observe
##### Build the app with Docker in Azure Cloud Shell and push the image to Azure Container Registry

1. In CloudShell, cd to helloworld-observe
```
cd observability-examples/azure/container-apps/helloworld-observe
```
2. Build the Hello World sample app and push the image to the Azure Container Registry by running the following command:
```
az acr build --registry $ACR_NAME --image $APP_NAME .
```

3. Deploy the Hello World app to Azure Container Apps, using the following command.
```
az containerapp create \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $ENVIRONMENT \
  --image $ACR_NAME.azurecr.io/$APP_NAME \
  --target-port 3500 \
  --ingress 'external' \
  --registry-server $ACR_NAME.azurecr.io \
  --query properties.configuration.ingress.fqdn
```
This command will output the deployed Hello World app's fully qualified domain name (FQDN). Copy and paste the FQDN into a browser to see the Hello World app running in Azure Container Apps.
