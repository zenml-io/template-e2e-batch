# 💫 ZenML End-to-End Tabular Training with Batch Predictions Project Template

What would you need to get a quick understanding of the ZenML framework and
start building your ML pipelines? The answer is a comprehensive project template
to cover major use cases of ZenML: a collection of steps and pipelines and, 
to top it all off, a simple but useful CLI. This is exactly
what the ZenML templates are all about.

This project template is a good starting point for anyone starting with ZenML.
It consists of two pipelines with the following high-level steps:
<p align="center">
  <img height=300 src="template/.assets/00_pipelines_composition.png">
</p>

* [CT] Training
  * Load, split, and preprocess the training dataset
  * Search for an optimal model architecture and tune its hyperparameters
  * Train the model and evaluate its performance on the holdout set
  * Compare a recently trained model with one used for inference and trained earlier
  * If a recently trained model - label it as a new inference model
* [CD] Batch Inference
  * Load the inference dataset and preprocess it in the same fashion as during the training
  * Perform data drift analysis
  * Run predictions using a model labeled as an inference model
  * Store predictions as an artifact for future use

It showcases the core ZenML concepts for supervised ML with batch predictions:

* designing [ZenML pipeline steps](https://docs.zenml.io/user-guide/starter-guide/create-an-ml-pipeline)
* using [step parameterization](https://docs.zenml.io/user-guide/starter-guide/create-an-ml-pipeline#parametrizing-a-step)
 and [step caching](https://docs.zenml.io/user-guide/starter-guide/cache-previous-executions#caching-at-a-step-level)
to design flexible and reusable steps
* using [custom data types for your artifacts and writing materializers for them](https://docs.zenml.io/user-guide/advanced-guide/artifact-management/handle-custom-data-types)
* constructing and running a [ZenML pipeline](https://docs.zenml.io/user-guide/starter-guide/create-an-ml-pipeline)
* accessing ZenML pipeline run artifacts in [the post-execution phase](https://docs.zenml.io/user-guide/starter-guide/fetch-runs-after-execution)
after a pipeline run has concluded
* best practices for implementing and running reproducible and reliable ML
pipelines with ZenML

In addition to that, the entire project is implemented with the [scikit-learn](https://scikit-learn.org)
library and showcases how to use ZenML with a popular ML framework. It makes
heavy use of the tabular datasets and classification models that scikit-learn
provides, but the concepts and patterns it showcases apply to any
other ML framework.

## 📃 Template Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| Name | The name of the person/entity holding the copyright | ZenML GmbH |
| Email | The email of the person/entity holding the copyright | info@zenml.io |
| Project Name | Short name for your project | ZenML E2E project |
| Project Version | The version of your project | 0.0.1 |
| Project License | The license under which your project will be released (one of `Apache Software License 2.0`, `MIT license`, `BSD license`, `ISC license`, `GNU General Public License v3` and `Not open source`) | Apache Software License 2.0 |
| Technical product name | The technical name to prefix all tech assets (pipelines, models, etc.) | e2e_use_case |
| Target environment | The target environment for deployments/promotions (one of `staging`, `production`) | staging |
| Use hyperparameter tuning | Whether to use hyperparameter tuning or not | yes |
| Use metric-based promotion | Whether to compare metric of interest to make model version promotion | yes |
| Use data quality checks | Whether to use data quality checks based on Evidently report to assess data before inference | yes |
| Notifications on failure | Whether to notify about pipelines failures | yes |
| Notifications on success | Whether to notify about pipelines successes | no |
| Auto-Format | Whether to automatically format and cleanup the generated code with [black](https://black.readthedocs.io/), [ruff](https://beta.ruff.rs/docs/) and [autoflake](https://github.com/PyCQA/autoflake) (yes/no). You also need to have these Python packages installed for this option to take effect. | no |
| Remote ZenML Server URL | Optional URL of a remote ZenML server for support scripts | - |

## 🚀 Generate a ZenML Project

First, to use the templates, you need to have Zenml and its `templates` extras installed: 

```bash
pip install zenml[templates]
```

Now you can generate a project from one of the existing templates by using the `--template` flag with the `zenml init` command:

```bash
zenml init --template <short_name_of_template>
# example: zenml init --template e2e_batch
```

Running the command above will result in input prompts being shown to you. If you would like to rely on default values for the ZenML project template - you can add `--template-with-defaults` to the same command, like this:

```bash
zenml init --template <short_name_of_template> --template-with-defaults
# example: zenml init --template e2e_batch --template-with-defaults
```

## 🧰 How this template is implemented

We will be going section by section diving into implementation details and sharing tips and best practices along this journey.

### [Continuous Training] Training Pipeline: ETL steps

[📂 Code folder](template/steps/etl/)
<p align="center">
  <img height=500 src="assets/01_etl.png">
</p>

Usually at the very beginning of every training pipeline developers are acquiring data to work with in later stages. In this example, we are using [the Breast Cancer Dataset](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_breast_cancer.html) to showcase steps but avoid high computational costs.

The first `data_loader` step is downloading data, which is passed to the `train_data_splitter` step responsible for splitting into train and test to avoid target leakage on data cleaning. The next `train_data_preprocess` step is preparing a `sklearn.Pipeline` object based on the training dataset and applying it also on the testing set to form ready-to-use datasets.

We also output `preprocess_pipeline` as an output artifact from `train_data_preprocess` - it will be passed into the inference pipeline later on, to prepare the inference data using the same fitted pipeline from training. Sklearn `Pipeline` comes really handy to perform consistent repeatable data manipulations on top of pandas `DataFrame` or similar structures.

### [Continuous Training] Training Pipeline: Model architecture search and hyperparameter tuning

[📂 Code folder](template/steps/%7B%25%20if%20hyperparameters_tuning%20%25%7Dhp_tuning%7B%25%20endif%20%25%7D)
<p align="center">
  <img height=400 src="assets/02_hp.png">
</p>

To ensure the high quality of ML models many ML Engineers go for automated hyperparameter tuning or even automated model architecture search. In this example, we are using prepared data from ETL to spin up a search of the best model parameters for different architectures in parallel.

To create parallel processing of computationally expensive operations we use a loop over predefined potential architectures and respective parameters search grid and create one step for each candidate. After the steps are created we need to collect results (one best model per each search step) in a `hp_tuning_select_best_model` step to define the final winner and pass it to training. To ensure that collection goes smoothly and in full we use an `after` statement populated with all search steps names, so the selector job will wait for the completion of all searches.

You can find more information about the current state of [Hyperparameter Tuning using ZenML in the documentation](https://docs.zenml.io/user-guide/advanced-guide/pipelining-features/hyper-parameter-tuning).

Another important concept introduced at this stage is [Custom Materializers](https://docs.zenml.io/user-guide/advanced-guide/artifact-management/handle-custom-data-types#custom-materializers): `hp_tuning_single_search` produce an output containing best parameters as a normal python dictionary and model architecture as a sklearn model class. Implementation of `ModelInfoMaterializer` is [here](template/artifacts/materializer.py).

Later on, this materializer class is passed into steps to create such an output explicitly.
<details>
  <summary>Code snippet 💻</summary>

```python
@step(output_materializers=ModelInfoMaterializer)
def hp_tuning_select_best_model(
    search_steps_prefix: str,
) -> Annotated[Dict[str, Any], "best_model"]:
  ...
```
</details>


### [Continuous Training] Training Pipeline: Model training and evaluation

[📂 Code folder](template/steps/training/)
<p align="center">
  <img height=500 src="assets/03_train.png">
</p>

Having the best model architecture and its hyperparameters defined in the previous stage makes it possible to train a quality model. Also, model training is the right place to bring an [Experiment Tracker](https://docs.zenml.io/user-guide/component-guide/experiment-trackers) into the picture - we will log all metrics and model itself into the [Experiment Tracker](https://docs.zenml.io/user-guide/component-guide/experiment-trackers), so we can register our model in a [Model Registry](https://docs.zenml.io/user-guide/component-guide/model-registries) and pass it down to a [Model Deployer](https://docs.zenml.io/user-guide/component-guide/model-deployers) easily and traceable. We will use information from Active Stack to make implementation agnostic of the underlying infrastructure.
<details>
  <summary>Code snippet 💻</summary>

```python
experiment_tracker = Client().active_stack.experiment_tracker
@step(experiment_tracker=experiment_tracker.name)
def model_trainer(
    ...
) -> Annotated[ClassifierMixin, "model"]:
  ...
```
</details>
Even knowing that the hyperparameter tuning step happened we would like to ensure that our model meets at least minimal quality standards - this quality gate is on the evaluation step. In case the model is of low-quality metric-wise an Exception will be raised and the pipeline will stop.

To notify maintainers of our Data Product about failures or successful completion of a pipeline we use [Alerter](https://docs.zenml.io/user-guide/component-guide/alerters) of the active stack. For failures it is convenient to use pipeline hook `on_failure` and for successes, a step notifying about it added as a last step of the pipeline comes in handy.
<details>
  <summary>Code snippet 💻</summary>

```python
alerter = Client().active_stack.alerter

def notify_on_failure() -> None:
    alerter.post(message=build_message(status="failed"))

@step(enable_cache=False)
def notify_on_success() -> None:
    alerter.post(message=build_message(status="succeeded"))

@pipeline(on_failure=notify_on_failure)
def e2e_example_training(...):
  ...
  promote_metric_compare_promoter(...)
  notify_on_success(after=["promote_metric_compare_promoter"])
```
</details>


### [Continuous Training] Training Pipeline: Model promotion

[📂 Code folder](template/steps/promotion/)
<p align="center">
  <img height=500 src="assets/04_promotion.png">
</p>

Once the model is trained and evaluated on meeting basic quality standards, we would like to understand whether it is good enough to beat the existing model used in production. This is a very important step, as promoting a weak model in production might result in huge losses at the end of the day.

In this example, we are implementing metric compare promotion to decide on the spot and avoid more complex approaches like Champion/Challengers shadow deployments. In other projects, other promotion techniques and strategies can vary.

To achieve this we would retrieve the model version from [Model Registry](https://docs.zenml.io/user-guide/component-guide/model-registries): latest (the one we just trained) and current (the one having a proper tag). Next, we need to deploy both models using [Model Deployer](https://docs.zenml.io/user-guide/component-guide/model-deployers) and run predictions on the testing set for both of them. Next, we select which one of the model versions has a better metric value and associate it with the inference tag. By doing so we ensure that the best model version would be used for inference later on.

### [Continuous Deployment] Batch Inference

<p align="center">
  <img height=500 src="assets/05_batch_inference.png">
</p>

### [Continuous Deployment] Batch Inference: ETL Steps

[📂 Code folder](template/steps/etl)

The process of loading data is similar to training, even the same step function is used, but with the `is_inference` flag.

But inference flow has an important difference - there is no need to fit preprocessing `Pipeline`, rather we need to reuse one fitted during training on the train set, to ensure that model gets the expected input. To do so we will use [ExternalArtifact](https://docs.zenml.io/user-guide/advanced-guide/pipelining-features/configure-steps-pipelines#pass-any-kind-of-data-to-your-steps) with lookup by `pipeline_name` and `artifact_name` - it will return ensure that required artifact is properly passed in inference preprocessing.
<details>
  <summary>Code snippet 💻</summary>

```python
########## ETL stage  ##########
df_inference, target = data_loader(is_inference=True)
df_inference = inference_data_preprocessor(
    dataset_inf=df_inference,
    preprocess_pipeline=ExternalArtifact(
        pipeline_name=MetaConfig.pipeline_name_training,
        artifact_name="preprocess_pipeline",
    ),
    target=target,
)
```
</details>


### [Continuous Deployment] Batch Inference: Drift reporting

[📂 Code folder](template/steps/%7B%25%20if%20data_quality_checks%20%25%7Ddata_quality%7B%25%20endif%20%25%7D)

On the drift reporting stage we will use [standard step](https://docs.zenml.io/stacks-and-components/component-guide/data-validators/evidently#the-evidently-data-validator) `evidently_report_step` to build Evidently report to assess certain data quality metrics. `evidently_report_step` has a number of options, but for this example, we will build only `DataQualityPreset` metrics preset to get a number of NA values in reference and current datasets.

After the report is built we execute another quality gate using the `drift_na_count` step, which assesses if a significant drift in NA count is observed. If so, execution is stopped with an exception.

You can follow [Data Validators docs](https://docs.zenml.io/user-guide/component-guide/data-validators) to get more inspiration on how and when to use drift detection in your pipelines.

### [Continuous Deployment] Batch Inference: Inference

[📂 Code folder](template/steps/inference)

As a last step concluding all work done so far, we will calculate predictions on the inference dataset and persist them in [Artifact Store](https://docs.zenml.io/user-guide/component-guide/artifact-stores) for reuse.

As we performed promotion as part of the training pipeline it is very easy to fetch the needed model version from [Model Registry](https://docs.zenml.io/user-guide/component-guide/model-registries) and deploy it for inference with [Model Deployer](https://docs.zenml.io/user-guide/component-guide/model-deployers).

Once the model version is deployed the only thing left over is to call `.predict()` on the deployment service object and put those predictions as an output of the predictions step, so it is automatically stored in [Artifact Store](https://docs.zenml.io/user-guide/component-guide/artifact-stores) with zero effort.
<details>
  <summary>Code snippet 💻</summary>

```python
@step
def inference_predict(
    deployment_service: MLFlowDeploymentService,
    dataset_inf: pd.DataFrame,
) -> Annotated[pd.Series, "predictions"]:
    predictions = deployment_service.predict(request=dataset_inf)
    predictions = pd.Series(predictions, name="predicted")
    return predictions
```
</details>
