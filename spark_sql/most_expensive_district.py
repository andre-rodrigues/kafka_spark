from pyspark.sql import SparkSession
from pyspark.sql.functions import *


if __name__ == "__main__":
    # Initialise spark session
    spark = SparkSession.builder.appName("Pyspark most expensive district in NY") \
        .master("local[*]") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    # Add the necessary lines to find the most expensive district/Borough in NY
    # ...
