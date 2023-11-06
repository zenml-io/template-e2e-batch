# {% include 'template/license_header' %}

from steps import (
    data_loader,
{%- if data_quality_checks %}
    drift_quality_gate,
{%- endif %}
    inference_data_preprocessor,
    inference_predict,
    notify_on_failure,
    notify_on_success,
)
from zenml import pipeline
from zenml.integrations.evidently.metrics import EvidentlyMetricConfig
from zenml.integrations.evidently.steps import evidently_report_step
from zenml.logger import get_logger
from zenml.artifacts.external_artifact import ExternalArtifact

logger = get_logger(__name__)


@pipeline(on_failure=notify_on_failure)
def {{product_name}}_batch_inference():
    """
    Model batch inference pipeline.

    This is a pipeline that loads the inference data, processes
    it, analyze for data drift and run inference.
    """
    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    # Link all the steps together by calling them and passing the output
    # of one step as the input of the next step.
    ########## ETL stage  ##########
    df_inference, target, _ = data_loader(
        random_state=ExternalArtifact(
            model_artifact_pipeline_name="e2e_use_case_training",
            model_artifact_name="random_state",
        ),
        is_inference=True
    )
    df_inference = inference_data_preprocessor(
        dataset_inf=df_inference,
        preprocess_pipeline=ExternalArtifact(
            model_artifact_name="preprocess_pipeline",
        ),
        target=target,
    )

{%- if data_quality_checks %}
    ########## DataQuality stage  ##########
    report, _ = evidently_report_step(
        reference_dataset=ExternalArtifact(
            model_artifact_name="dataset_trn",
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
    inference_predict(
        dataset_inf=df_inference,
{%- if data_quality_checks %}
        after=["drift_quality_gate"],
{%- endif %}
    )

    notify_on_success(after=["inference_predict"])
    ### YOUR CODE ENDS HERE ###
