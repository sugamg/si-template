# Databricks notebook source
##Dataset 

# COMMAND ----------

wine_dataset = "default.winequality1"
soil_dataset = "db2"
file_server = "esft.gsk.com"
dataset_for_scoring = "abfss://root@coedapus6abfsuat001.dfs.core.windows.net/data/trusted/dpe-nonconf/corp/global/datahub/wine_quality_incr"
dataset_for_model_comparison = "abfss://root@coedapus6abfsprod001.dfs.core.windows.net/data/trusted/dpe-nonconf/corp/global/datahub/wine_quality_for_comparison"

# COMMAND ----------

##parameters and metrics

# COMMAND ----------

parameters = {"alpha": 0.75, "l1_ratio_1": 0.25}
metrics_name =  "rmse"
metrics_higher_is_better = False



# COMMAND ----------

## path configurations

# COMMAND ----------

experiment_name = "/my-experiment"
output_path = "/dbfs/outputs/"
model_path = "models"
unit_tests_results_path = "/dbfs/tmp/test-reports"
integration_tests_results_base_path = "abfss://root@coedapus6abfsuat001.dfs.core.windows.net/data/trusted/dpe-nonconf/corp/datascience" 

# COMMAND ----------

## model information

# COMMAND ----------

model_name = "wine-quality"
model_version = ''

# COMMAND ----------

## test scoring
target_column = "quality"
target_column_type =  "string"
num_rows_for_scoring = 50

# COMMAND ----------

## compliance
description =  "Model for XYZ"
tags = {"engineering": "ML Platform",
        "release.candidate": "DPE",
        "release.version": "1.0.0"}
