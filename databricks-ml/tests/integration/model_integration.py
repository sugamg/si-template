# Databricks notebook source
# MAGIC %md # Test model integration
# MAGIC 
# MAGIC The goal of this notebook is to make sure the end-to-end process doesn't break.

# COMMAND ----------

# MAGIC %md 
# MAGIC ### Import required configs from existing config notebook
# MAGIC Make sure to update the configs prior to a run

# COMMAND ----------

#  PLEASE DO NOT REMOVE THE LINES BELOW

# COMMAND ----------

# MAGIC %run "../../app/notebooks/model_train"

# COMMAND ----------

import mlflow
from mlflow.tracking.client import MlflowClient
from pyspark.sql import functions as F

model_name_for_scoring = model_name  # from model_conf 

# COMMAND ----------

# MAGIC %md ## Make predictions on test data

# COMMAND ----------

df = spark.read.format('delta').load(dataset_for_scoring)

# COMMAND ----------

client = MlflowClient()
if (model_version == '' or model_version is None):
  model_version = client.get_latest_versions(model_name, stages=['None'])[0].version
model_udf = mlflow.pyfunc.spark_udf(spark, f"models:/{model_name}/None",result_type=target_column_type)

# COMMAND ----------

# make it a smaller dataset
df = df.limit(num_rows_for_scoring)

# COMMAND ----------

preds = (
  df
    .withColumn(target_column, model_udf(*df.columns))
    .withColumn("model_version", F.lit(model_version))
)


# COMMAND ----------

results_path = f"{integration_tests_results_base_path}/models/{model_name}/{model_version}/scoring"

# COMMAND ----------

#write results to dbfs location
preds.write \
  .format("delta") \
  .mode("overwrite") \
  .save(results_path)

# COMMAND ----------

#load the dataset with predictions
df_results = spark.read.format("delta").load(results_path)

if not (target_column in df_results.columns  and "model_version" in df_results.columns):
  raise Exception(f"Scoring failed for model = {model_name}, version = {model_version}")
else:
  print(f"Scoring succeeded for model = {model_name}, version = {model_version}")

# COMMAND ----------


