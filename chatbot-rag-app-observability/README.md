# Running Elasticsearch Chatbot-rag-app with EDOT on Docker and K8s

This repo and instructions are for running [Chatbot RAG App](https://github.com/elastic/elasticsearch-labs/tree/main/example-apps/chatbot-rag-app) with Elastic Cloud using either Docker or Kubernetes

Elastic’s sample [RAG based Chatbot application](https://github.com/elastic/elasticsearch-labs/tree/main/example-apps/chatbot-rag-app), showcases how to use Elasticsearch with local data that has embeddings, enabling search to properly pull out the most contextual information during a query with a chatbot connected to an LLM of your choice.  It’ a great example of how to build out a RAG based application with Elasticsearch. 

This app is also now insturmented with EDOT, and you can visualize the Chatbot’s traces to OpenAI, as well as relevant logs, and metrics from the application. By running the app as instructed in the github repo with Docker you can see these traces on a local stack. But how about running it against serverless, Elastic cloud or even with Kubernetes?

## Prerequisites

These few pre-requisites are needed to ensure you can run on with Elastic Cloud for Kubernetes or Docker

1. An Elastic Cloud account — sign up now, and become familiar with Elastic’s OpenTelemetry configuration. With Serverless no version required. With regular cloud minimally 8.17

2. Git clone the RAG based Chatbot application and go through the tutorial on how to bring it up and become more familiar and how to bring up the application using Docker.

3. An account on OpenAI with API keys

4. Kubernetes cluster - use Amazon EKS, Google GKE, or Microsoft Azure AKS.

5. Be familiar with EDOT to understand how we bring in logs, metrics, and traces from the application through the OTel Collector


# Run chatbot-rag-app on K8s

In order to set this up, you can follow the following repo on Observability-examples which has the Kubernetes yaml files being used. These will also point to Elastic Cloud.


1. Set up the Kubernetes Cluster

2. Create a docker image using the Dockerfile from the repo. However use the following build command to ensure it will run on any K8s environment.,

```bash
docker buildx build --platform linux/amd64 -t chatbot-rag-app .
```

3. Push the image to your favorite container repo

4. Get the appropriate ENV variables:

- Find the OTEL_EXPORTER_OTLP\_ENDPOINT/HEADER variables in your Elastic Cloud instance under `integrations-->APM` 

- Get your OpenAI Key

- Get the Elasticsearch URL, username and password.

5. Replace the variables and your image location in both `init-index-job.yaml` and `k8s-deployment.yaml`


Here is what you replace in `k8s-deployment.yaml`

```bash
stringData:
  ELASTICSEARCH_URL: "https://yourelasticcloud.es.us-west-2.aws.found.io"
  ELASTICSEARCH_USER: "elastic"
  ELASTICSEARCH_PASSWORD: "elastic"
  OTEL_EXPORTER_OTLP_HEADERS: "Authorization=Bearer%20xxxx"
  OTEL_EXPORTER_OTLP_ENDPOINT: "https://12345.apm.us-west-2.aws.cloud.es.io:443"
  OPENAI_API_KEY: "YYYYYYYY"

  AND

spec:
      containers:
      - name: chatbot-regular
#Replace your image location here
        image: yourimagelocation:latest
```
Here is what you replace in `init-index-job.yaml`

```bash
    spec:
      containers:
      - name: init-index
#update your image location for chatbot rag app
        image: your-image-location:latest
```

6. Then run the following

```bash
kubectl create -f k8s-deployment.yaml
kubectl create -f init-index-job.yaml
```

Here is what happens:

- `k8s-deployment.yaml` will ensure the chatbot-rag-app pods are running
-  `k8s-deployment.yaml` deploys a secret with your env variables (OpenAI key, Elastic end points, OTel endpoint and header, etc)
-  `init-index-job.yaml` will run a job initializing elasticsearch with the index for the app, and use the secret created by k8s-deployment.yaml

6. Once the job iscomplete and the chatbot-rag-app is running, get the loadbalancer url by running:

```bash
kubectl get services
```

You should see something such as:
```bash
NAME                                 TYPE           CLUSTER-IP       EXTERNAL-IP                                                               PORT(S)                                                                     AGE
chatbot-regular-service            LoadBalancer   10.100.130.44    xxxxxxxxx-1515488226.us-west-2.elb.amazonaws.com   80:30748/TCP    
                                                            6d23h
```

7. Open the URL and run the app, then log into Elastisearch Cloud and look for your service in APM.


## Running chatbot-rag-app on Docker

1. Get the appropriate ENV variables:

- Find the OTEL_EXPORTER_OTLP\_ENDPOINT/HEADER variables in your Elastic Cloud instance under `integrations-->APM` 

- Get your OpenAI Key

- Get the Elasticsearch URL, username and password.

2. Replace the variables a local copy of `env.example` - DO NOT FORGET TO call it `.env`

3. Run `docker compose up --build --force-recreate`

4. Play with app at `localhost:4000`

5. Log into Elastisearch Cloud and look for your service in APM.

