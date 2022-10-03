# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="http://gsk.com/assets/img/gsk-logo.png" alt="GSK" style="width: 150px">
# MAGIC   <img src="https://upload.wikimedia.org/wikipedia/commons/6/63/Databricks_Logo.png" alt="Databricks" style="width: 250px">
# MAGIC </div>

# COMMAND ----------

# MAGIC %md 
# MAGIC ### Import required configs from existing config notebook
# MAGIC Make sure to update the configs prior to a run

# COMMAND ----------

# MAGIC %run "./app/conf/configs"

# COMMAND ----------

try:
  dbutils.notebook.run("./app/notebooks/01_get_data", 3600, {'train_flag' : "True"})
  print("Data imported. Bronze table created.")
except Exception as e:
  print("Error importing data.")


# COMMAND ----------


## CLEAN THE TRAINING DATA ## Expected runtime: ~5 mins
if pipeline['clean_data']is True:
  try:
    print("Cleaning data...")
    dbutils.notebook.run("./notebooks/02_data_cleaning", 6000, {'train_flag' : "True"})
    print("Data cleaned. Silver table created.")
  except Exception as e:
    print("Error cleaning data.")
else: print("Skipping data cleaning.")
    
## ENGINEER FEATURES ## Expected runtime: ~5 mins
if pipeline['feature_engineering']is True:
  try:
    print("Engineering features for modeling...")
    dbutils.notebook.run("./notebooks/03_feature_engineering", 6000, {'train_flag' : "True"})
    print("Features engineered. Gold table created.")
  except Exception as e:
    print("Error engineering features.")
else: print("Skipping feature engineering.")

## SELECT THE BEST MODELS ## Expected runtime: 1+ hours depending on max_evals parameter
if pipeline['model_selection']is True:
  try:
    print("Running hyperopt to select best models & parameters...")
    dbutils.notebook.run("./notebooks/04_model_selection", 0)
    print("Best models selected. Saved best params to file.")
  except Exception as e:
    print("Error selecting models.")
else: print("Skipping model selection.")

## TRAIN AND REGISTER FINAL MODELS ## Expected runtime: ~5 mins  
if pipeline['model_training']is True:
  try:
    print("Training final models...")
    dbutils.notebook.run("./notebooks/05_final_model_training", 6000)
    print("Models trained and registered in Model Registry")
  except Exception as e:
    print("Error training models.")
else: print("Skipping model training.")

## SCORE CUSTOMERS ## Expected runtime: ~2 mins  
if pipeline['scoring']is True:
  try:
    print("Scoring customers...")
    dbutils.notebook.run("./notebooks/06_scoring", 0, {'train_flag' : "False"})
    print(f"Customers scored and results saved to {scoring_output_table}")
  except Exception as e:
    print("Error scoring customers.")
else: print("Skipping scoring.")