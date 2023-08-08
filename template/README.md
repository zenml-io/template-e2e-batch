# {{project_name}}

This is a comprehensive supervised ML project built with the
ZenML framework and its integration. The project trains one or more
scikit-learn classification models to make predictions on the tabular
classification datasets provided by the scikit-learn library. The project was
generated from the [E2E Batch ZenML project template](https://github.com/zenml-io/template-e2e-batch)
with the following properties:
- Project name: {{project_name}}
- Technical Name: {{product_name}}
- Version: `{{version}}`
{%- if open_source_license %}
- Licensed with {{open_source_license}} to {{full_name}}<{{email}}>
{%- endif %}
- Deployment environment: `{{target_environment}}`
{%- if zenml_server_url!='' %}
- Remote ZenML Server URL: `{{zenml_server_url}}`
{%- endif %}

Settings of your project are:
{%- if hyperparameters_tuning %}
- Hyperparameters and model architecture tuning using configuration from `config.py`
{%- else %}
- Fixed model architecture defined in `config.py`
{%- endif %}
{%- if metric_compare_promotion %}
- Trained model promotion to `{{target_environment}}` based on accuracy metric vs currently deployed model
{%- else %}
- Every trained model will be promoted to `{{target_environment}}`
{%- endif %}
{%- if data_quality_checks %}
- Data drift checks based on Evidently report
{%- endif %}
{%- if notify_on_failures and notify_on_successes %}
- Notifications about failures and successes enabled
{%- elif notify_on_failures %}
- Notifications about failures enabled
{%- elif notify_on_successes %}
- Notifications about success enabled
{%- else %}
- All notifications disabled
{%- endif %}

## 👋 Introduction

Welcome to your newly generated "{{project_name}}" project! This is
a great way to get hands-on with ZenML using production-like template. 
The project contains a collection of standard and custom ZenML steps, 
pipelines and other artifacts and useful resources that can serve as a 
solid starting point for your smooth journey with ZenML.

What to do first? You can start by giving the the project a quick run. The
project is ready to be used and can run as-is without any further code
changes! You can try it right away by installing ZenML, the needed
ZenML integration and then calling the CLI included in the project. We also
recommend that you start the ZenML UI locally to get a better sense of what
is going on under the hood:

```bash
# Set up a Python virtual environment, if you haven't already
python3 -m venv .venv
source .venv/bin/activate
# Install requirements & integrations
make setup
# Start the ZenML UI locally (recommended, but optional);
# the default username is "admin" with an empty password
zenml up
# Run the pipeline included in the project
python run.py
```

When the pipelines are done running, you can check out the results in the ZenML
UI by following the link printed in the terminal (or you can go straight to
the [ZenML UI pipelines run page](http://127.0.0.1:8237/workspaces/default/all-runs?page=1).

Next, you should:

* look at the CLI help to see what you can do with the project:
```bash
python run.py --help
```
* go back and [try out different parameters](https://github.com/zenml-io/template-e2e-batch#-template-parameters)
for your generated project. For example, you could disable hyperparameters
tuning and use your favorite model architecture or promote every trained model,
if you haven't already!
* take a look at [the project structure](#📜-project-structure) and the code
itself. The code is heavily commented and should be easy to follow.
* read the [ZenML documentation](https://docs.zenml.io) to learn more about
various ZenML concepts referenced in the code and to get a better sense of
what you can do with ZenML.
* start building your own ZenML project by modifying this code

## 📦 What's in the box?

The {{project_name}} project demonstrates how the most important steps of 
the ML Production Lifecycle can be implemented in a reusable way remaining 
agnostic to the underlying infrastructure, and how to integrate them together 
into pipelines serving Training and Batch Inference purposes.

This template uses 
[the Breast Cancer Dataset](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_breast_cancer.html)
to demonstrate how to perform major critical steps for Continuous Training (CT)
and Continuous Delivery (CD).

It consists of two pipelines with the following high-level steps:
<p align="center">
  <img height=300 src=".assets/00_pipelines_composition.png">
</p>

* [CT] Training
  * Load, split and preprocess the training dataset
  * Search an optimal model architecture and tune its' hyperparameters
  * Train the model and evaluate its performance on the holdout set
  * Compare recently trained model with one used for inference and trained earlier
  * If recently trained model - label it as a new inference model
* [CD] Batch Inference
  * Load the inference dataset and preprocess it in the same fashion as during the training
  * Perform data drift analysis
  * Run predictions using a model labeled as an inference model
  * Store predictions as an artifact for future use

In [the repository documentation](https://github.com/zenml-io/template-e2e-batch#-how-this-template-is-implemented),
you can find more details about every step of this template.

The project code is meant to be used as a template for your projects. For
this reason, you will find several places in the code specifically marked
to indicate where you can add your code:

```python
### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
...
### YOUR CODE ENDS HERE ###
```

## 📜 Project Structure

The project loosely follows [the recommended ZenML project structure](https://docs.zenml.io/user-guide/starter-guide/follow-best-practices):

```
.
├── artifacts               # handler for Custom Materializers
├── pipelines               # `zenml.pipeline` implementations
│   ├── batch_inference.py  # [CD] Batch Inference pipeline
│   └── training.py         # [CT] Training Pipeline
├── steps                   # logically grouped `zenml.steps` implementations
│   ├── alerts              # alert developer on pipeline status
│   ├── data_quality        # quality gates built on top of drift report
│   ├── etl                 # ETL logic for dataset
│   ├── hp_tuning           # tune hyperparameters and model architectures
│   ├── inference           # inference on top of the model from the registry
│   ├── promotion           # find if a newly trained model will be new inference
│   └── training            # train and evaluate model
├── utils                   # helper functions
├── .dockerignore
├── config.py               # default configuration of Pipelines
├── Makefile                # helper scripts for quick start with integrations
├── README.md               # this file
├── requirements.txt        # extra Python dependencies 
└── run.py                  # CLI tool to run pipelines on ZenML Stack
```
