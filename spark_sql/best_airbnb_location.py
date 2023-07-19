from pyspark.sql import SparkSession
from pyspark.sql.functions import *


if __name__ == "__main__":
    # Initialise spark session
    spark = SparkSession.builder.appName("Pyspark best Airbnb in NY") \
        .master("local[*]") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    # Read datasets
    complaints_df = spark.read \
        .option("header", True) \
        .csv("datasets/nyc_noise_complaints.csv")

    airbnb_df = spark.read \
        .option("header", True) \
        .csv("datasets/nyc_airbnb_2019.csv")

    # Create temporary views 
    complaints_df.createOrReplaceTempView("complaints")
    airbnb_df.createOrReplaceTempView("airbnbs")

    # Query with SQL
    spark.sql("""
        SELECT lower(neighbourhood_group) as district, *
        FROM airbnbs
        WHERE price < 100 AND room_type = 'Entire home/apt'
    """).createOrReplaceTempView("cheap_places")

    spark.sql("""
        SELECT lower(Borough) as district, count(*) as noise_complaints_in_district
        FROM complaints
        GROUP BY lower(Borough)
    """).createOrReplaceTempView("complaints_by_district")

    spark.sql("""
        SELECT noise_complaints_in_district, district, name, price, number_of_reviews
        FROM cheap_places
        LEFT JOIN complaints_by_district USING(district)
        ORDER BY noise_complaints_in_district ASC, price ASC;
    """).show(10, False)






