# {% include 'template/license_header' %}

from datetime import datetime as dt
import os
from typing import Optional

from zenml.artifacts.external_artifact import ExternalArtifact
from zenml.logger import get_logger

from pipelines import {{product_name}}_batch_inference, {{product_name}}_training

logger = get_logger(__name__)


def main(
    no_cache: bool = False,
    no_drop_na: bool = False,
    no_normalize: bool = False,
    drop_columns: Optional[str] = None,
    test_size: float = 0.2,
    min_train_accuracy: float = 0.8,
    min_test_accuracy: float = 0.8,
    fail_on_accuracy_quality_gates: bool = False,
    only_inference: bool = False,
):
    """Main entry point for the pipeline execution.

    This entrypoint is where everything comes together:

      * configuring pipeline with the required parameters
        (some of which may come from command line arguments)
      * launching the pipeline

    Args:
        no_cache: If `True` cache will be disabled.
        no_drop_na: If `True` NA values will not be dropped from the dataset.
        no_normalize: If `True` normalization will not be done for the dataset.
        drop_columns: List of comma-separated names of columns to drop from the dataset.
        test_size: Percentage of records from the training dataset to go into the test dataset.
        min_train_accuracy: Minimum acceptable accuracy on the train set.
        min_test_accuracy: Minimum acceptable accuracy on the test set.
        fail_on_accuracy_quality_gates: If `True` and any of minimal accuracy
            thresholds are violated - the pipeline will fail. If `False` thresholds will
            not affect the pipeline.
        only_inference: If `True` only inference pipeline will be triggered.
    """

    # Run a pipeline with the required parameters. This executes
    # all steps in the pipeline in the correct order using the orchestrator
    # stack component that is configured in your active ZenML stack.
    pipeline_args = {
        "config_path":os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "config.yaml",
            )
        }
    if no_cache:
        pipeline_args["enable_cache"] = False

    if not only_inference:
        # Execute Training Pipeline
        run_args_train = {
            "drop_na": not no_drop_na,
            "normalize": not no_normalize,
            "random_seed": 42,
            "test_size": test_size,
            "min_train_accuracy": min_train_accuracy,
            "min_test_accuracy": min_test_accuracy,
            "fail_on_accuracy_quality_gates": fail_on_accuracy_quality_gates,
        }
        if drop_columns:
            run_args_train["drop_columns"] = drop_columns.split(",")

        pipeline_args[
            "run_name"
        ] = f"{{product_name}}_training_run_{dt.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        {{product_name}}_training.with_options(**pipeline_args)(**run_args_train)
        logger.info("Training pipeline finished successfully!")

    # Execute Batch Inference Pipeline
    run_args_inference = {}
    pipeline_args[
        "run_name"
    ] = f"{{product_name}}_batch_inference_run_{dt.now().strftime('%Y_%m_%d_%H_%M_%S')}"
    {{product_name}}_batch_inference.with_options(**pipeline_args)(**run_args_inference)

    artifact = ExternalArtifact(
        pipeline_name="{{product_name}}_batch_inference",
        artifact_name="predictions",
    )
    logger.info(
        "Batch inference pipeline finished successfully! "
        "You can find predictions in Artifact Store using ID: "
        f"`{str(artifact.get_artifact_id())}`."
    )