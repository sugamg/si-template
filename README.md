**Demo - MLOps for Databricks ML**

**Steps**:
- Create a git repo from template. 
	- Add "DataServices" in Settings/Collaborators&Teams. 
	- Add Branch rules: 
		- Require a pull request before merging/Require Approvals 
		- Require status checks to pass before merging, add approproiate mlops pipeline for this check
	- In ADO, create a new pipeline selecting the main yml file from the above git repo (check feasibility running via COPro)
	- Hooks: Either add manually in git Settings, or launch the pipeline manually for the first run only
- Provide user-defined variables
    - databricks-ml/app/conf/model_config.py : All config towards dataset input/output, target column, model name, model path, model parameters, model metrics, model tags(towards compliance checks), inputs for scoring etc
- Use notebook templates for developing models
	- databricks-ml/app/notebooks/load_cleanse_data.py: Use this for loading datasets/data cleansing
	- databricks-ml/app/notebooks/feature_engineering.py: Use this for feature engineering, final dataset to be "df"
	- databricks-ml/app/notebooks/model_train.py: Add your model code here
- Build your own unit tests
	- databricks-ml/tests/unit/test_feature_engineering.py: A sample has been provided to run unit tests using unittest. Save test report (shall be used for automation)
- Integration and compliance tests
	- databricks-ml/tests/integration/model_integration.py: A sample has been provided to deploy code, train, register model and simulate batch inferencing. Saves the results with predictions into dbfs in a user defined path and verified version of model used for scoring
	- databricks-ml/tests/integration/compliance_test.py: This checks for tags applied for the Model version. Tags should be provided in model_config.py


**MLOps paradigm**: Deploy Code

**Environments**: Development, UAT, Prod 

**Trigger: Feature branch**
- Deploy in Dev
	- Deploy code
	- Model training
	- Register model
	- Run unit testing
- Deploy in UAT
	- Run integration tests
		- Deploy code
		- Model training 
		- Register model
		- Batch inferencing and verify model version used for prediction
- Merge PR to main

**Trigger: Release branch**
- Deploy in Prod
	- Deploy code
	- Model training
	- Register model ('None')
	- Run compliance checks, transition model to 'Staging'
	- Model comparison - using sample dataset, get predictions from both Staging and Production models and evaluate metrics
	- Transition model to 'Production' (iff new model performs better)



