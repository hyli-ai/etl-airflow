# Project: Data Pipelines with Airflow

## Introduction
A music streaming company, Sparkify, has decided that it is time to introduce more automation and monitoring to their data warehouse ETL pipelines and come to the conclusion that the best tool to achieve this is Apache Airflow.

The goal of this project is to create high grade data pipelines that are dynamic and built from reusable tasks, can be monitored, and allow easy backfills. Data quality also plays a big part when analyses are executed on top the data warehouse and need to run tests against their datasets after the ETL steps have been executed to catch any discrepancies in the datasets.

The source data resides in S3 and needs to be processed in Sparkify's data warehouse in Amazon Redshift. The source datasets consist of JSON logs that tell about user activity in the application and JSON metadata about the songs the users listen to.

## Project Template
The project template includes three files:

1. The `dag template` has all the imports and task templates in place, but the task dependencies have not been set
2. The `operators` folder with operator templates
3. A `helper class` for the SQL transformations

## File Location
The input files are located in the following S3 buckets:
- Song data: s3://udacity-dend/song_data
- Log data: s3://udacity-dend/log_data

## Instructions
### Configuring the DAG
In the DAG, add default parameters according to these guidelines

+ The DAG does not have dependencies on past runs
+ On failure, the task are retried 3 times
+ Retries happen every 5 minutes
+ Catchup is turned off
+ Do not email on retry

### Building the operators
To complete the project, four different operators that will stage the data, transform the data, and run checks on data quality are required.

All of the operators and task instances will run SQL statements against the Redshift database. However, using parameters wisely will allow you to build flexible, reusable, and configurable operators you can later apply to many kinds of data pipelines with Redshift and with other databases.

#### Stage Operator
The stage operator is expected to be able to load any JSON formatted files from S3 to Amazon Redshift. The operator creates and runs a SQL COPY statement based on the parameters provided. The operator's parameters should specify where in S3 the file is loaded and what is the target table.

The parameters should be used to distinguish between JSON file. Another important requirement of the stage operator is containing a templated field that allows it to load timestamped files from S3 based on the execution time and run backfills.

#### Fact and Dimension Operators
With dimension and fact operators, utilize the provided SQL helper class to run data transformations. Most of the logic is within the SQL transformations and the operator is expected to take as input a SQL statement and target database on which to run the query against. Define a target table that will contain the results of the transformation.

Dimension loads are often done with the truncate-insert pattern where the target table is emptied before the load. Thus, it would be useful to have a parameter that allows switching between insert modes when loading dimensions. Fact tables are usually so massive that they should only allow append type functionality.

#### Data Quality Operator
The final operator to create is the data quality operator, which is used to run checks on the data itself. The operator's main functionality is to receive one or more SQL based test cases along with the expected results and execute the tests. For each the test, the test result and expected result needs to be checked and if there is no match, the operator should raise an exception and the task should retry and fail eventually.

For example one test could be a SQL statement that checks if certain column contains NULL values by counting all the rows that have NULL in the column. We do not want to have any NULLs so expected result would be 0 and the test would compare the SQL statement's outcome to the expected result.


### Steps to process:
1. Run command `/opt/airflow/start.sh` and start Airflow UI when the web server is ready.
2. Go to the AWS console, create an IAM user with administrative access.
3. Copy the Access Key ID and Secret Access Key, and create a connection in Airflow UI using these info.
4. Go back to the AWS console, switch the Region to US-West-2, and create a cluster in Redshift. (Would need to create a default VPC if it does not exist)
5. Make this cluster publicly accessible (for the simplicity to connect to it in this project).
6. Modify the Security group attached to the cluster, and allow inbound traffic from 0.0.0.0/0 (All traffic)
7. Use the Query Editor in AWS console, connect to the database.
8. Paste the create_tables.sql provided in this project into the editor and run it. This will create all the necessary Tables.
9. Copy the Redshift Endpoint and add another connection in Airflow UI.
10. On the Airflow UI, toggle the switch on the DAG from off to on, and trigger the DAG.


