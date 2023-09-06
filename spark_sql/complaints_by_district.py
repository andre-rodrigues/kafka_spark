import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.postgresql:postgresql:42.5.4 pyspark-shell'

from pyspark.sql import SparkSession
from pyspark.sql.functions import *


if __name__ == "__main__":
    # Initialise spark session
    spark = SparkSession.builder.appName("Pyspark complaints by district in NY") \
        .master("local[*]") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    # Read dataset
    complaints_df = spark.read \
        .option("header", True) \
        .csv("datasets/nyc_noise_complaints.csv")

    # Run aggregations and show results.

    #######
    # Option 1: Using python functions to run aggregations
    ####### 
    complaints_df.groupBy(col("Borough")).count().show(100, False)

    #######
    # Option 2: Using SQL to run aggregations
    ####### 
    complaints_df.createOrReplaceTempView("complaints")

    results = spark.sql("""
        SELECT Borough, count(*) as count
        FROM complaints
        GROUP BY Borough;
    """)

    # Write to console
    results.show(100, False)

    # Write to Database
    results.write \
        .format("jdbc") \
        .mode("append") \
        .option("url", "jdbc:postgresql://waia-spark-sql-db:5432/waia") \
        .option("driver", "org.postgresql.Driver") \
        .option("dbtable", "complaints") \
        .option("user", "postgres") \
        .option("password", "postgres") \
        .save()

