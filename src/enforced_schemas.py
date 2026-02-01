from pyspark.sql.types import *

schema = StructType([
    StructField("Order ID", IntegerType(), True),
    StructField("Product", StringType(), True),
    StructField("Quantity Ordered", IntegerType(), True),
    StructField("Price Each", DoubleType(), True),
    StructField("Order Date", StringType(), True),
    StructField("Purchase Address", StringType(), True)
])