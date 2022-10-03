# Databricks notebook source
import pyspark.sql.functions as f

# COMMAND ----------

def engineer_features(df):
	return df.withColumn("total_acidity", f.col("fixed acidity") + f.col("volatile acidity"))

def rename_columns(df):
	renamed_columns = [f.col(col_name).alias(col_name.replace(" ", "_")) for col_name in df.columns]
	return df.select(renamed_columns)

# COMMAND ----------

def loadBronzeTable(path, data_format):
  
  """
  Reads an existing table from Redshift in as a Spark Dataframe
  
  """
  
  # Import our customer data table
  raw_data = spark.read.format(data_format).option("header", "true").option("sep", ";").load(path)
  features = engineer_features(raw_data)
  data = rename_columns(features)

  return data
