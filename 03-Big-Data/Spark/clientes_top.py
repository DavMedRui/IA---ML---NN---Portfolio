from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as sum, col, count

spark = SparkSession.builder.appName("ClientesTop").getOrCreate()

df = spark.read.option("header", True).option("delimiter", ";").csv("ventasOnline.csv")

df = df.withColumn("Total", col("Quantity") * col("UnitPrice"))

clientes_top = df.groupBy("CustomerID", "Country").agg(sum("Total").alias("GastoTotal"),
    count("InvoiceNo").alias("NumeroCompras")
    ).filter(col("CustomerID").isNotNull()).orderBy(col("GastoTotal").desc()).limit(10)

clientes_top.show(truncate=False)

spark.stop()