# Databricks notebook source
# MAGIC %md 
# MAGIC # Compare models in stages Production and Staging (i.e., candidate for new deployment)
# MAGIC This notebook contains code for scoring using a small data sample as part of an experiement. Hence please use mlflow
# MAGIC 
# MAGIC Pre-requisites:
# MAGIC You have provided the necessary parameters towards the scoring and metrics to be used in model_config notebook
# MAGIC 
# MAGIC NOTE:
# MAGIC - If this is the first time deployment, perform scoring, evaluate metrics  and transition model to 'Production'
# MAGIC - If there is already an existing model in 'Production', then do the following:
# MAGIC   - perform scoring for model in 'Production' and evaluate metrics defined in model_config (say, rmse and specify lower is better)
# MAGIC   - perform scoring for model in 'Staging' and evaluate metrics  
# MAGIC   - compare the metrics from the above steps. If the model in 'Production' performs better, then do not promote the new model candidate (in 'Staging'). Else, transition the newer model version from 'Staging' to 'Production' and the previous model verion from 'Production' to 'Archived'

# COMMAND ----------

# Please add your metrics evaluation code here
# BEGIN

# COMMAND ----------

import numpy as np
from sklearn.metrics import mean_squared_error
def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    return rmse

# COMMAND ----------

# END

# COMMAND ----------

# PLEASE DO NOT REMOVE THE CODE BELOW

# COMMAND ----------

# MAGIC %run ../conf/model_config

# COMMAND ----------

# dataset being used for scoring
df = spark.read.format('delta').load(dataset_for_model_comparison)
df = df.limit(num_rows_for_scoring)
test = df.toPandas()

df_x = test.drop([f"{target_column}"], axis=1)
df_y = test[[f"{target_column}"]]

# COMMAND ----------

import mlflow
import pandas as pd
import pyspark.sql
from mlflow.tracking import MlflowClient

# COMMAND ----------

#retrieve the version numbers for models in 'Production' and 'Staging'
first_deployment = False

client = MlflowClient()
if (model_version == '' or model_version is None):
  staging_model_version = client.get_latest_versions(model_name, stages=['Staging'])[0].version
  
production_model = client.get_latest_versions(model_name, stages=['Production'])

# there are no models in Production, so its the first time deployment
if (not production_model):
  first_deployment = True


# COMMAND ----------

# Perform scoring process for the new model being developed which is in 'Staging'
model_staging = mlflow.pyfunc.load_model(f"models:/{model_name}/{staging_model_version}")
better_model = "Staging"
experiment_id = mlflow.set_experiment(experiment_name)
with mlflow.start_run():
  #get predictions from Staging version
  prediction_staging = model_staging.predict(df_x)
  #calculate metrics for staging predictions
  metrics_staging = eval_metrics(df_y, prediction_staging)
  mlflow.log_metric(f"{metrics_name}_staging", metrics_staging)
  
  #No models in Prod, deploying the model in prod environment for the first time
  if(first_deployment):
    print(f"First time deployment. Promoting the Staging model with {metrics_name}={metrics_staging} to Production")
  else:
    #get predictions from Production version
    model_production = mlflow.pyfunc.load_model(f"models:/{model_name}/Production")
    prediction_production = model_production.predict(df_x)
    #calculate metrics for production predictions
    metrics_production = eval_metrics(df_y, prediction_production)
    mlflow.log_metric(f"{metrics_name}_production", metrics_production)  

    # deploy the better performing model
    if not (metrics_higher_is_better) and (metrics_production <= metrics_staging):
      print(f"Current Production model with {metrics_name}={metrics_production} performs better than/same as Staging model with {metrics_name}={metrics_staging}")
      #retain prod
      better_model = "Production"
    else:
      #make staging to prod, prod to archive
      print(f"Promoting the Staging model with {metrics_name}={metrics_staging} to Production. Archiving the current Production model")

dbutils.notebook.exit(better_model)

# COMMAND ----------


