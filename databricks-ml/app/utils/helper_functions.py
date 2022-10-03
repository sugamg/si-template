# Databricks notebook source
import pyspark.sql.functions as f
import pickle
import os

# COMMAND ----------

def saveDfToDelta(df, db_name, delta_table_name, partition = None):
  
  """
  Takes a spark df and saves it to the metastore as a delta table
  If the db_name provided doesn't exist, it will be created. 
  
  """
  
  # Create database if it doesn't already exist
  database_creation = f"CREATE DATABASE IF NOT EXISTS {db_name};"
  spark.sql(database_creation)
  
  #Write the data to the metastore as a delta table
  if partition is None:
    df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f'{db_name}.{delta_table_name}')
  else:
    (df.write.format("delta").partitionBy(partition)
                         .mode("overwrite")
                         .option("overwriteSchema", "true")
                         .saveAsTable(f'{db_name}.{delta_table_name}')
    )
      
def save_obj(obj, path, name ):
  """
  Saves a python object as a pickle file
  """
  if not os.path.exists(path):
    os.makedirs(path)
  with open(path + name + '.pkl', 'wb') as f:
      pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(path, name):
  """
  Reads a pickled object
  """
  with open(path + name + '.pkl', 'rb') as f:
      return pickle.load(f)


# COMMAND ----------

def read_data(path, filename, scaler = None):  
  """
  This method reads numpy data from disk

  :param path: The path to the file containing the data
  :param filename: The name of the file containing the data 
  :return: ids, features, target numpy arrays, and column names
  """  
  pd_df = pd.read_pickle(path + filename)

  ids = pd_df[['email_uid']]
  target = pd_df[['target']]
  features = pd_df.iloc[:, 2:]

  features_dummies = pd.get_dummies(features)
  if scaler is None:
      scaler = StandardScaler().fit(features_dummies)
  features_scaled = scaler.transform(features_dummies)
  
  return ids, features_scaled, target, features_dummies.columns, scaler
