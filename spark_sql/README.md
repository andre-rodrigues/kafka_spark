# Spark SQL

Spark SQL is a component of Apache Spark with which users can write SQL queries to interact with distributed datasets, enabling data manipulation and analysis.

Overall, Spark SQL simplifies big data processing by providing a familiar SQL interface and leveraging the distributed processing power of Apache Spark.

Feel free to run some of the scripts in this repository to see how it works and explore the source code.

### Example using Docker:

```
docker compose up
```


### Example without Docker:

```
pip install -r requirements.txt

python complaints_by_district.py
```

You should see a result like this in your terminal.

```
+-------------+-----+
|Borough      |count|
+-------------+-----+
|Unspecified  |980  |
|QUEENS       |38274|
|BROOKLYN     |68905|
|BRONX        |47672|
|MANHATTAN    |64172|
|STATEN ISLAND|5411 |
+-------------+-----+
```
