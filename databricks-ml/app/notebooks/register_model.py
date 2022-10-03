# Databricks notebook source
# MAGIC %run "../conf/model_config"

# COMMAND ----------

# MAGIC %run "../utils/helper_functions"

# COMMAND ----------

# MAGIC %run "../utils/model_registry"

# COMMAND ----------

model_name = "wine-quality"
experiment_name = "/my-experiment"
metric = 'rmse'
model_artifact_name = 'model'
model = register_best_model(model_name, experiment_name, metric, order_by="ASC", model_artifact_name=model_artifact_name)

# COMMAND ----------

print(model)
