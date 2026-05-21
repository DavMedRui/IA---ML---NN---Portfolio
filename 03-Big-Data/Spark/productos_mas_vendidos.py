from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as spark_sum, col

spark = SparkSession.builder.appName("ProductosMasVendidos").getOrCreate()

df = spark.read.option("header", True).option("delimiter", ";").csv("ventasOnline.csv")

productos_mas_vendidos = df.groupBy("StockCode", "Description") \
    .agg(spark_sum("Quantity").alias("CantidadTotal")) \
    .orderBy(col("CantidadTotal").desc()) \
    .limit(10)

productos_mas_vendidos.show(truncate=False)

spark.stop()