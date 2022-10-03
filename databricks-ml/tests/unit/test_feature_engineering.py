# Databricks notebook source
# MAGIC %md 
# MAGIC # Unit testing
# MAGIC This notebook runs any unit tests as part of MLOps prior to deploying model into the staging/UAT environment
# MAGIC 
# MAGIC Pre-requisites:
# MAGIC - Make sure you have updated the relevant variables in the Configs notebook.
# MAGIC 
# MAGIC NOTE:
# MAGIC - Refer to the sample unit testcase. unittest framework has been used here

# COMMAND ----------

# Install any libraries used HERE
%pip install unittest-xml-reporting

# COMMAND ----------

# PLEASE DO NOT REMOVE THE LINE BELOW

# COMMAND ----------

# MAGIC %run  "../../app/conf/model_config"

# COMMAND ----------

# Add your unit tests below
# BEGIN

# COMMAND ----------

# MAGIC %run "../../app/utils/import_data"

# COMMAND ----------

# MAGIC %run "../../app/utils/helper_functions"

# COMMAND ----------

import unittest

# COMMAND ----------

from pyspark.sql import SparkSession

class FeatureEngineering(unittest.TestCase):

  def test_preprocess(self):
      spark = SparkSession.builder.getOrCreate()

      df = spark.createDataFrame([[2.8, 3.1], [0.0, 20.2]]).toDF("fixed acidity", "volatile acidity")
      actual_df = df.transform(engineer_features)

      expected_df = spark.createDataFrame(
          [
              [2.8, 3.1, 5.9],
              [0.0, 20.2, 20.2],
          ]
      ).toDF("fixed acidity", "volatile acidity", "total_acidity")

      self.assertEqual(actual_df.collect(),expected_df.collect())


# COMMAND ----------

def discover_test_cases(*test_classes):
  suite = unittest.TestSuite()
  for test_class in test_classes:
    for test in unittest.defaultTestLoader.getTestCaseNames(test_class):
      suite.addTest(test_class(test))
      
  return suite

# COMMAND ----------

suite = discover_test_cases(FeatureEngineering)


# COMMAND ----------

# if we want to generate JUnit-compatible output, set to True
use_xml_runner = True

if use_xml_runner:
  import xmlrunner
  runner = xmlrunner.XMLTestRunner(output=unit_tests_results_path)
else:
  runner = unittest.TextTestRunner()
results = runner.run(suite)

# COMMAND ----------

dbutils.fs.ls(unit_tests_results_path.replace('/dbfs', 'dbfs:'))

# COMMAND ----------

#END
