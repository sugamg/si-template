# Databricks notebook source
# MAGIC %md 
# MAGIC # Develop and train model
# MAGIC This notebook is mainly used for model development and training.  
# MAGIC Pre-requisites: 
# MAGIC - Make sure you have updated the relevant variables in the Configs notebook.
# MAGIC 
# MAGIC NOTE: 
# MAGIC - This notebook assumes that you have completed the data loading, data cleansing and feature engineering tasks using the templates provided in the repo
# MAGIC - We recommend the use of mlflow logging - experiments, metrics, parameters, model and any artifacts
# MAGIC - You'll need to evaluate metrics and log them using mlflow since this shall be used in automated tests to compare model performance : Staging vs Production
# MAGIC - This notebook automatically registers the model into the Model Registry
# MAGIC - Tags defined in the model_config would be automatically applied on the registered model

# COMMAND ----------

# PLEASE DO NOT REMOVE THE LINES BELOW

# COMMAND ----------

# MAGIC %run "./feature_engineering"

# COMMAND ----------

# PLEASE ADD YOUR CODE BELOW
# BEGIN

# COMMAND ----------

import os
import warnings
import sys

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet

import mlflow
import mlflow.sklearn


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


def train_model(alpha, l1_ratio, model_path, experiment_name):
    warnings.filterwarnings("ignore")
    np.random.seed(40)

    # Read the wine-quality csv file (make sure you're running this from the root of MLflow!)
    #data = pd.read_csv(wine_data_path, sep=None)
    data = df.toPandas()

    # Split the data into training and test sets. (0.75, 0.25) split.
    train, test = train_test_split(data)

    # The predicted column is "quality" which is a scalar from [3, 9]
    train_x = train.drop(["quality"], axis=1)
    test_x = test.drop(["quality"], axis=1)
    train_y = train[["quality"]]
    test_y = test[["quality"]]
    experiment_id = mlflow.set_experiment(experiment_name)
    # Start a new MLflow training run 
    with mlflow.start_run():
        # Fit the Scikit-learn ElasticNet model
        lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
        lr.fit(train_x, train_y)

        predicted_qualities = lr.predict(test_x)

        # Evaluate the performance of the model using several accuracy metrics
        (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

        print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        # Log model hyperparameters and performance metrics to the MLflow tracking server
        # (or to disk if no)
        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)

        mlflow.sklearn.log_model(lr, model_path)
        
        return mlflow.active_run().info.run_uuid

# COMMAND ----------

# alpha = 0.75
# l1_ratio_1 = 0.25
alpha = parameters['alpha']
l1_ratio_1  = parameters['l1_ratio_1']
run_id = train_model(alpha, l1_ratio_1,  model_path, experiment_name)

# COMMAND ----------

#  END

# COMMAND ----------

# PLEASE DO NOT REMOVE THE LINES BELOW

# COMMAND ----------

model_uri = f"runs:/{run_id}/{model_path}"

# COMMAND ----------

# Register the model
import time
model = mlflow.register_model(
    model_uri,
    model_name
)
time.sleep(10)

# COMMAND ----------

# Set tags configured by user
import mlflow
client = mlflow.tracking.MlflowClient()

if (tags):
  for tag in tags:
    client.set_model_version_tag(model.name, model.version, tag, tags[tag])
