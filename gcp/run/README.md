# Elastic Observability Helloworld Demo App for Google Cloud Run

## Overview

This demo application has two parts: 
* helloworld - A simple Node.js express app
* helloworld-observe - A helloworld Node.js app instrumented with minimal Elastic Observability

---

### Setup

1. Create an [Elastic Cloud Deployment](https://cloud.elastic.co)
   * In Elastic Cloud, select **Integrations** from the top-level menu. Then click the **APM** integrations tile.
   * Copy the Elastic APM **serverUrl** and save it for a later step.
   * Copy the Elastic APM **secretToken** and save it for a later step.



2. Enable necessary [Google Cloud APIs](https://console.cloud.google.com/flows/enableapi?apiid=compute.googleapis.com,,run.googleapis.com,containerregistry.googleapis.com,cloudbuild.googleapis.com)
   * compute.googleapis.com
   * run.googleapis.com
   * containerregistry.googleapis.com
   * cloudbuild.googleapis.com


3. Add required [IAM](https://console.cloud.google.com/iam-admin/) roles to the Google Compute Engine Default Service Account
   * Logs Viewer
   * Monitoring Viewer
   * Pub/Sub Subscriber


### Deploy to Google Cloud Run from Google Cloud Shell


Open [Google Cloud Shell](https://console.cloud.google.com/cloudshell) and clone this repo
```
git clone https://github.com/elastic/observability-examples

```

---

#### helloworld
1. In Google Cloud Shell, cd to helloworld
    ```
    cd gcp/run/helloworld
    ```
2. Build helloworld app image and push it to Google Container Resistry
    ```
    gcloud builds submit --tag gcr.io/your-project-id/elastic-helloworld
    ```
3. Deploy helloworld app to Google Cloud Run
    ```
    gcloud run deploy elastic-helloworld --image gcr.io/your-project-id/elastic-helloworld
    ```
4. Once the app is deployed, a Service URL will be provided. Open the Service URL in a browser to see the helloworld app running.

---

#### helloworld-observe

1. In Google Cloud Shell, cd to helloworld-observe
    ```
    cd gcp/run/helloworld-observe
    ```
2. Update `Dockerfile` to add the Elastic Observability APM **Server URL** and the APM **Secret Token**. Replace **ELASTIC_APM_SERVER_URL** and **ELASTIC_APM_SECRET_TOKEN** with values you copied and saved in the **Setup** step.
   ```
    ENV OTEL_EXPORTER_OTLP_ENDPOINT='ELASTIC_APM_SERVER_URL'
    ENV OTEL_EXPORTER_OTLP_HEADERS='Authorization=Bearer ELASTIC_APM_SECRET_TOKEN'
   ```

3. Build helloworld-observe app image and push it to Google Container Resistry
    ```
    gcloud builds submit --tag gcr.io/your-project-id/elastic-helloworld
    ```
4. Deploy helloworld-observe app to Google Cloud Run
    ```
    gcloud run deploy elastic-helloworld --image gcr.io/your-project-id/elastic-helloworld
    ```
5. Once the app is deployed, a Service URL will be provided. Open the Service URL in a browser to see the helloworld-observe app running.
6. Visit [Elastic Cloud](https://cloud.elastic.co/home) and open **Observability** to see Trace samples from the helloworld-observe app.
