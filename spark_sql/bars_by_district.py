from pyspark.sql import SparkSession
from pyspark.sql.functions import *


if __name__ == "__main__":
    # Initialise spark session
    spark = SparkSession.builder.appName("Pyspark bars by district in NY") \
        .master("local[*]") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    # Add the necessary lines to calculate the number of bars per district/Borough
    # ...
