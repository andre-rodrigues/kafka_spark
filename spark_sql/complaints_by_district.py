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
    spark.sql("""
        SELECT Borough, count(*) as count
        FROM complaints
        GROUP BY Borough;
    """).show(100, False)

