# Data Pipelines with Airflow
>
In this project, a set of automated data pipelines is created using Apache Airflow, with the source data resides in S3 and processed Amazon Redshift. Custom operators are created in an Airflow dag to stage the data, fill the data warehouse, and run checks on the data.

## Table of contents

* [Introduction](#introduction)
* [Project Description](#project-description)
* [Dataset](#dataset)
* [Project Instructions](#project-instructions)
* [Files in this Project](#files-in-this-project)
* [Steps to Process](#steps-to-process)

## Introduction

### Scenario
A music streaming company, Sparkify, has decided that it is time to introduce more automation and monitoring to their data warehouse ETL pipelines and come to the conclusion that the best tool to achieve this is Apache Airflow.

### Goal
* They goal of this project, as a data engineer, is to create high grade data pipelines that are dynamic and built from reusable tasks, can be monitored, and allow easy backfills.

* Data quality plays a big part when analyses are executed on top the data warehouse. It would be desirable to run tests against their datasets after the ETL steps have been executed to catch any discrepancies in the datasets.

* The source data resides in S3 and needs to be processed in Sparkify's data warehouse in Amazon Redshift. The source datasets consist of JSON logs that tell about user activity in the application and JSON metadata about the songs the users listen to.

## Project Description
* Create custom operators to perform tasks such as staging the data, filling the data warehouse, and running checks on the data as the final step.

* Data imports, custom operators, and a set of tasks that are linked to achieve a coherent and sensible data flow within the pipeline are all contained in the python file located in `\dags\sparkify_data_pipeline.py`.

* A helpers class that contains all the SQL transformations is also provided and needs to be executed with custom operators.

## Dataset
Two sets of data are presented: the **Song Dataset** and the **Log Dataset**. These datasets reside in S3, and here are the S3 links for each:

* Song data: `s3://udacity-dend/song_data`
* Log data: `s3://udacity-dend/log_data`

## Project Instructions

### Configuring the DAG
In the DAG, these `default parameters` are added:

1. The DAG does not have dependencies on past runs.
2. On failure, the task are retried 3 times.
3. Retries happen every 5 minutes.
4. Catchup is turned off.
5. Do not email on retry.

The task dependencies are configured so that after the dependencies are set, the graph view follows the flow shown in the image below.

![Airflow_dag](/images/airflow_correct_dag.png)

### Building the operators
Four different operators are built to stage the data, transform the data, and run checks on data quality.

All of the operators and task instances will run SQL statements against the Redshift database. However, using parameters wisely will allow you to build flexible, reusable, and configurable operators you can later apply to many kinds of data pipelines with Redshift and with other databases.

#### Stage Operator
The stage operator is expected to be able to load any JSON formatted files from S3 to Amazon Redshift. The operator creates and runs a SQL COPY statement based on the parameters provided. The operator's parameters should specify where in S3 the file is loaded and what is the target table.

The parameters should be used to distinguish between JSON file. Another important requirement of the stage operator is containing a templated field that allows it to load timestamped files from S3 based on the execution time and run backfills.

#### Fact and Dimension Operators
With dimension and fact operators, you can utilize the provided SQL helper class to run data transformations. Most of the logic is within the SQL transformations and the operator is expected to take as input a SQL statement and target database on which to run the query against. You can also define a target table that will contain the results of the transformation.

Dimension loads are often done with the truncate-insert pattern where the target table is emptied before the load. Thus, you could also have a parameter that allows switching between insert modes when loading dimensions. Fact tables are usually so massive that they should only allow append type functionality.

#### Data Quality Operator
The final operator to create is the data quality operator, which is used to run checks on the data itself. The operator's main functionality is to receive one or more SQL based test cases along with the expected results and execute the tests. For each the test, the test result and expected result needs to be checked and if there is no match, the operator should raise an exception and the task should retry and fail eventually.

For example one test could be a SQL statement that checks if certain column contains NULL values by counting all the rows that have NULL in the column. We do not want to have any NULLs so expected result would be 0 and the test would compare the SQL statement's outcome to the expected result.

#### Note about Workspace
 Run `/opt/airflow/start.sh` command to start the Airflow web server. Once the Airflow web server is ready, click on the blue `Access Airflow` button to access the Airflow UI.

## Files in this Project
The project contains three major components:

1. File `dags\sparkify_data_pipeline.py` is the dag which has all the imports, task, task dependencies.

2. The `plugin\operators` folder with four operator:
    * `stage_redshift.py`
    * `load_fact.py`
    * `load_dimension.py`
    * `data_quality.py`

3. A `helper class` with a file `plugins\helpers\sql_queries.py` for the SQL transformations.

## Steps to process:
1. Run command `/opt/airflow/start.sh` and start Airflow UI when the web server is ready.

2. Go to the AWS console, create an IAM user with administrative access.

3. Copy the **Access Key ID** and **Secret Access Key**, and create a connection in Airflow UI using these info.

4. Go back to the AWS console, switch the Region to **US-West-2**, and create a cluster in Redshift. (Would need to create a default VPC if it does not exist)

5. Make this cluster publicly accessible (for the simplicity to connect to it in this project).

6. Modify the Security group attached to the cluster, and allow inbound traffic from 0.0.0.0/0 (All traffic)

7. Use the **Query Editor** in AWS console, connect to the database.

8. Paste the `create_tables.sql` provided in this project into the editor and run it. This will create all the necessary Tables.

9. Copy the Redshift Endpoint and add another connection in Airflow UI.

10. On the Airflow UI, toggle the switch on the DAG from off to on, and trigger the DAG.


