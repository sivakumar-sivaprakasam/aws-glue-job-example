import sys
from awsglue.transforms import Join
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col
glueContext = GlueContext(SparkContext.getOrCreate())
job = Job(context)
job.init(args['JOB_NAME'], args)
	
spark = SparkSession.builder.config("spark.jars", "/home/siva/postgresql-42.2.26.jar").getOrCreate()

raw_country_df = spark.read.format("com.databricks.spark.csv").option("header", "true").option("inferSchema", "true").option("delimiter", ";").load("/home/siva/dataset/country.csv")
new_country_df = raw_country_df.rdd.zipWithIndex().toDF()
new_country_df = new_country_df.select((col("_2")+1).alias("country_id"), col("_1.country_name"))
new_country_df.show()

new_country_df.write.format("jdbc").option("url", "jdbc:postgresql://172.25.16.1:5432/testdb?currentSchema=test").option("driver", "org.postgresql.Driver").option("dbtable", "country").option("user", "postgres").option("password", "postgres").mode("append").save()

raw_employee_df = spark.read.format("com.databricks.spark.csv").option("header", "true").option("inferSchema", "true").option("delimiter", ";").load("/home/siva/dataset/employee_list.csv")
raw_employee_df.printSchema()
raw_employee_df.show()

merged_emp_df = raw_employee_df.join(raw_country_df, raw_employee_df.country_id == raw_country_df.country_id, "left").drop(raw_employee_df.country_id).drop(raw_country_df.country_id)

db_country_df = spark.read.format("jdbc").option("url", "jdbc:postgresql://172.25.16.1:5432/testdb?currentSchema=test").option("driver", "org.postgresql.Driver").option("dbtable", "country").option("user", "postgres").option("password", "postgres").load()

db_country_df.show()

merged_emp_df = merged_emp_df.join(db_country_df, merged_emp_df.country_name == db_country_df.country_name).select(merged_emp_df.employee_id, merged_emp_df.employee_name, db_country_df.country_id, merged_emp_df.employee_type, merged_emp_df.employee_status)

merged_emp_df.write.format("jdbc").option("url", "jdbc:postgresql://172.25.16.1:5432/testdb?currentSchema=test").option("driver", "org.postgresql.Driver").option("dbtable", "employee").option("user", "postgres").option("password", "postgres").mode("append").save()

job.commit()