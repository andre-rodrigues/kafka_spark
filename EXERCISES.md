# Exercises

## Spark + Kafka

1- Explore the existing scripts and make changes on it.
- Change the topic name (currently `waia-events`) to something else. Make sure that `example_1` works with all options (printing to console, saving CSV files and saving in the database)
- Change the producer script by adding new names to the list and changing the format of the message published to Kafka. Make sure `example_1` works after that.

2- Create a project that will load data from Kafka to a table in a database.
- Use the `docker-compose.yml` in `/kafka` folder as reference to start a Kafka broker.
- Use the `docker-compose.yml` in `/spark_streaming` folder as reference to start a Postgres Database.
- Use the `producer` script as reference to create your own script to send data to a Kafka topic.
- Once you have the previous steps up and running, you'll be able to create a consumer.
- Create a consumer using Spark-Streaming to read data from Kafka and write to a table in a database. Use the script in the `example_1` folder as refence.



## Spark SQL

1- Add the necessary lines to calculate the number of bars per district/Borough (`bars_by_district.py`)

2- Add the necessary lines to find the most expensive district/Borough in NY (`most_expensive_district.py`)

3- Adjust the scripts to write the results to a database.
