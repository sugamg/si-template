# Databricks notebook source
# MAGIC %md 
# MAGIC # Read required data 
# MAGIC This notebook loads all the input dataset required for training the model
# MAGIC 
# MAGIC Pre-requisites:
# MAGIC - Make sure you have updated the relevant variables in the Configs notebook.

# COMMAND ----------

# The following shall be used if run as a pipeline
dbutils.widgets.text("train_flag", "True")
train_flag = dbutils.widgets.get('train_flag')
if train_flag == 'True':
  train_flag = True
else: train_flag = False

# COMMAND ----------

#PLEASE DO NOT REMOVE THE LINE BELOW

# COMMAND ----------

# MAGIC %run ../conf/model_config

# COMMAND ----------

# Load your datasets here. You may use model_config to add parameters for input dataset paths
# BEGIN

# COMMAND ----------

try:
  df = spark.sql(f"select * from {wine_dataset}") # use path as parameter
except Exception as e:
  print("Could not read the datasets. Check table has been created as expected.")

# COMMAND ----------

# END
