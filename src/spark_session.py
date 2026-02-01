from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("DataEngineeringProject")
    .master("local[*]")
    .getOrCreate()
)

print("Spark version:", spark.version)

spark.stop()
