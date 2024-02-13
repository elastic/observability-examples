# Elastic Observability Hello World Demo App for AWS App Runner

## Overview

This demo application has two parts: 
* helloworld - A simple Python Flask app
* helloworld-observe - A helloworld Python Flask app instrumented with minimal Elastic Observability

---

### Setup

1. Create an [Elastic Cloud Deployment](https://cloud.elastic.co)
   * In Elastic Cloud, select **Integrations** from the top-level menu. Then click the **APM** integrations tile.
   * Copy the Elastic APM **serverUrl** and save it for a later step.
   * Copy the Elastic APM **secretToken** and save it for a later step.

2. Install Docker in AWS CloudShell

    * Open [AWS Cloud Shell](https://console.aws.amazon.com/cloudshell/) and install Docker:
    ```
    sudo yum update -y
    sudo amazon-linux-extras install docker
    ```

    * Start the Docker daemon service:
    ```
    sudo dockerd
    ```

    * With Docker running, open a new tab in CloudShell. 
    * In the new CloudShell tab, authenticate Docker with AWS. Replace <account_id> with your AWS Account ID.
    ```
    aws ecr get-login-password --region us-east-2 | sudo docker login --username AWS --password-stdin <account_id>.dkr.ecr.us-east-2.amazonaws.com
    ```

3. In CloudShell, create an AWS ECR repository for the sample app image.
    ```
    aws ecr create-repository \
    --repository-name elastic-helloworld/web \
    --image-scanning-configuration scanOnPush=true \
    --region us-east-2
    ```

### Deploy the app to AWS App Runner
Clone this repo in CloudShell:
```
git clone https://github.com/elastic/observability-examples
```

---

#### helloworld
##### Build the app with Docker in AWS CloudShell and push the image to AWS ECR
1. In CloudShell, cd to helloworld
```
cd observability-examples/aws/app-runner/helloworld
```
2. Build the Hello World sample app:
```
sudo docker build -t elastic-helloworld/web .
```
3. Tag the application image with Docker. Replace <account_id> with your AWS Account ID.
```
sudo docker tag elastic-helloworld/web:latest <account_id>.dkr.ecr.us-east-2.amazonaws.com/elastic-helloworld/web:latest
```
4. Push the application image to AWS ECR. Replace <account_id> with your AWS Account ID.
```
sudo docker push <account_id>.dkr.ecr.us-east-2.amazonaws.com/elastic-helloworld/web:latest
```

##### Deploy the app to AWS App Runner
1. Open [AWS App Runner console](https://console.aws.amazon.com/apprunner/).

2. Click the **Create an App Runner service** button.
3. On the **Source and deployment page**, set the following deployment details:
  * In the **Source** section, for **Repository type**, choose **Container registry**.
    * For **Provider**, choose **Amazon ECR**
    * For **Container image URI**, choose **Browse** to select the Hello World application image previously pushed to AWS ECR.
      * In the **Select Amazon ECR container image** dialog box, for **Image repository**, select the "**elastic-helloworld/web**” repository.
      * For **Image tag**, select “**latest**”, and then choose **Continue**.
  * In the **Deployment settings** section, choose **Manual**.
  * For **ECR access role**, choose **Create new service role**.
  * Click the **Next** buttton.
4. On the **Configure service** page, in the **Service settings** section, enter the service name “**helloworld-app**” and click the **Next** button.
5. On the **Review and create** page, click **Create & deploy**.
6. Once the app is deployed, click the **Default domain** URL to view the helloworld app running.

---

#### helloworld-observe
##### Build the app with Docker in AWS CloudShell and push the image to AWS ECR
1. In CloudShell, cd to helloworld-observe
```
cd observability-examples/aws/app-runner/helloworld-observe
```
2. Build the Hello World sample app:
```
sudo docker build -t elastic-helloworld/web .
```
3. Tag the application image with Docker. Replace <account_id> with your AWS Account ID.
```
sudo docker tag elastic-helloworld/web:latest <account_id>.dkr.ecr.us-east-2.amazonaws.com/elastic-helloworld/web:latest
```
4. Push the application image to AWS ECR. Replace <account_id> with your AWS Account ID.
```
sudo docker push <account_id>.dkr.ecr.us-east-2.amazonaws.com/elastic-helloworld/web:latest
```

##### Deploy the app to AWS App Runner
1. Open [AWS App Runner console](https://console.aws.amazon.com/apprunner/).

2. Click the **Create an App Runner service** button.
3. On the **Source and deployment page**, set the following deployment details:
  * In the **Source** section, for **Repository type**, choose **Container registry**.
    * For **Provider**, choose **Amazon ECR**
    * For **Container image URI**, choose **Browse** to select the Hello World application image previously pushed to AWS ECR.
      * In the **Select Amazon ECR container image** dialog box, for **Image repository**, select the "**elastic-helloworld/web**” repository.
      * For **Image tag**, select “**latest**”, and then choose **Continue**.
  * In the **Deployment settings** section, choose **Manual**.
  * For **ECR access role**, choose **Create new service role**.
  * Click the **Next** buttton.
4. On the **Configure service** page, in the **Service settings** section, enter the service name “**elastic-helloworld-app**” and click the **Next** button.
5. On the **Review and create** page, click **Create & deploy**.
6. Once the app is deployed, click the **Default domain** URL to view the helloworld app running.

