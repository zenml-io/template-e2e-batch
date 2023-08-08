# {% include 'license_header' %}


from config import DEFAULT_PIPELINE_EXTRAS, PIPELINE_SETTINGS, MetaConfig
from steps import (
    data_loader,
{%- if data_quality_checks %}
    drift_quality_gate,
{%- endif %}
    inference_data_preprocessor,
    inference_get_current_version,
    inference_predict,
    notify_on_failure,
    notify_on_success,
)
from zenml import pipeline
from zenml.integrations.evidently.metrics import EvidentlyMetricConfig
from zenml.integrations.evidently.steps import evidently_report_step
from zenml.integrations.mlflow.steps.mlflow_deployer import (
    mlflow_model_registry_deployer_step,
)
from zenml.logger import get_logger
from zenml.steps.external_artifact import ExternalArtifact

logger = get_logger(__name__)


@pipeline(
    settings=PIPELINE_SETTINGS,
    on_failure=notify_on_failure,
    extra=DEFAULT_PIPELINE_EXTRAS,
)
def {{pipeline_name}}_batch_inference():
    """
    Model batch inference pipeline.

    This is a pipeline that loads the inference data, processes
    it, analyze for data drift and run inference.
    """
    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    # Link all the steps together by calling them and passing the output
    # of one step as the input of the next step.
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

{%- if data_quality_checks %}
    ########## DataQuality stage  ##########
    report, _ = evidently_report_step(
        reference_dataset=ExternalArtifact(
            pipeline_name=MetaConfig.pipeline_name_training,
            artifact_name="dataset_trn",
        ),
        comparison_dataset=df_inference,
        ignored_cols=["target"],
        metrics=[
            EvidentlyMetricConfig.metric("DataQualityPreset"),
        ],
    )
    drift_quality_gate(report)
{%- endif %}
    ########## Inference stage  ##########
    registry_model_version = inference_get_current_version()
    deployment_service = mlflow_model_registry_deployer_step(
        registry_model_name=MetaConfig.mlflow_model_name,
        registry_model_version=registry_model_version,
        replace_existing=False,
    )
    inference_predict(
        deployment_service=deployment_service,
        dataset_inf=df_inference,
{%- if data_quality_checks %}
        after=["drift_quality_gate"],
{%- endif %}
    )

    notify_on_success(after=["inference_predict"])
    ### YOUR CODE ENDS HERE ###
