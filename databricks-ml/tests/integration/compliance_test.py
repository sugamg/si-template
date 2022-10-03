# Databricks notebook source
# MAGIC %md 
# MAGIC # Compliance tests
# MAGIC This notebook runs any compliance tests as part of MLOps
# MAGIC 
# MAGIC Pre-requisites:
# MAGIC - Make sure you have updated the relevant variables in the Configs notebook.
# MAGIC 
# MAGIC NOTE:
# MAGIC - Refer to the sample below that mandates tags to be set for Registered Model before they are deployed to Production

# COMMAND ----------

# PLEASE DO NOT REMOVE THE LINE BELOW

# COMMAND ----------

# MAGIC %run ../../app/conf/model_config

# COMMAND ----------

# Add your compliance tests below
# BEGIN

# COMMAND ----------

import mlflow
client = mlflow.tracking.MlflowClient()

if (model_version == '' or model_version is None):
  model_version = client.get_latest_versions(model_name, stages=['None'])[0]
  
if (model_version):
  registered_tags =  model_version.tags
  
assert tags == registered_tags, "Compliance checks failed, no tags found"

# COMMAND ----------

# END
