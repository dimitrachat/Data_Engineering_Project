from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("SparkSanityCheck")
    .master("local[1]")
    .config("spark.ui.enabled", "false")
    .config("spark.sql.shuffle.partitions", "1")
    .config("spark.driver.memory", "1g")
    .getOrCreate()
)

print("Spark version:", spark.version)

spark.stop()
