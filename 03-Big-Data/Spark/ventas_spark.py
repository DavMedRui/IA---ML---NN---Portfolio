from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum

spark = SparkSession.builder.appName("ventas_pais").getOrCreate()

df = spark.read.csv("ventasOnline.csv", header=True, delimiter=";")

ventas_por_pais = df.withColumn("total", col("Quantity") * col("UnitPrice")) \
    .groupBy("Country") \
    .agg(spark_sum("total").alias("total_ventas")) \
    .orderBy(col("total_ventas").desc())

ventas_por_pais.show(41, truncate=False)

spark.stop()