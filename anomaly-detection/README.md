# Elastic Observability - Anomaly Detection transactions generator

## Overview
This code example generates 1000 example credit card transactions which include an anomaly that can be detected using Elastic’s anomaly detection tools.


### Setup
1. Node.js 
   
   Node.js is required to run this code example. See the instructions to download and install Node.js at [https://nodejs.org/en/download](https://nodejs.org/en/download) 

2. Elastic deployment

   Visit [cloud.elastic.co](https://cloud.elastic.co) to create a new deployment or use an existing deployment. Using an [Elastic Serverless](https://www.elastic.co/guide/en/serverless/current/serverless-get-started.html) observability project is recommended for a simple start.

3. Clone this repository

   Using a terminal, run the following command:
    ```
    git clone https://github.com/elastic/observability-examples
    ```

### Run the code example

1. Change directory to the code example folder:
    ```
    cd anomaly-detection
    ```

2. Install the code example’s dependencies:
    ```
    npm install
    ```

3. Run the code example to generate a JSON file named `transactions.ndjson` containing 1000 example transactions:
    ```
    node generate-transactions.js  
    ```

### Upload the transactions to an Elastic index

Complete the following steps to upload the generated `transactions.ndjson` file to an Elastic deployment which will create a new index.
   1. Within the Elastic Observability solution, select **Add data** from the left-navigation menu.  
   2. Select **Application** within the **What do you want to monitor** section.  
   3. In the **Search through other ways of ingesting data:** input field, enter the text `Upload`.  
   4. You should see the **Upload a file** tile appear. Select it.  
   5. On the **Upload data from a file** page, click the **Select or drag and drop a file** link.  
   6. In the file management window that appears, browse to and select the `transactions.ndjson` file that was created when you ran the `generate-transactions.js` code example.  
   7. You’ll then see a summary of the file contents that is to be imported. Click the **Import** button.  
   8. Enter a **Name** for the index that will be created and click the **Import** button.

### Create an Anomaly Detection Job

In your Elastic deployment create an Anomaly Detection Job using the index you created in the previous step.

   1. Within the Elastic Observability solution, select **Machine Learning \> Anomaly Detection \> Jobs** from the left-navigation menu.  
   2. On the **Select data view** page, select the index you created in the previous step.
   3. You’ll be prompted to select a job creation wizard. Select **Population**.  
   4. Within the **Create job: Population** wizard: 
      1. Select **Use full data** and click the **Next** button.  
      2. For the **Population** field, select **IPAddress** from the drop down menu.  
      3. For the **Add metric** field, select **Count(Event rate)**  
      4. You should see an initial graph of the data to be analyzed. Click the **Next** button.  
      5. On the **Job Details** page, enter a **Job ID**.  
      6. Click the **Next** button to proceed.  
      7. On the **Validation** page, click the **Next** button to view a summary of the job that is about to be created.  
      8. Click the **Create job** button. 
   5.  When the job creation is complete, click the **View Results** button.
   6.  This will open the **Anomaly Explorer** where you’ll be able to see the detected anomaly.