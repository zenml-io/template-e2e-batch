# {% include 'template/license_header' %}


from typing_extensions import Annotated

import pandas as pd
from zenml import step, get_step_context
from zenml.integrations.mlflow.steps.mlflow_deployer import (
    mlflow_model_registry_deployer_step,
)
from zenml.model import ArtifactConfig


@step
def inference_predict(
    dataset_inf: pd.DataFrame,
) -> Annotated[pd.Series, "predictions", ArtifactConfig(overwrite=False)]:
    """Predictions step.

    This is an example of a predictions step that takes the data in and returns
    predicted values.

    This step is parameterized, which allows you to configure the step
    independently of the step code, before running it in a pipeline.
    In this example, the step can be configured to use different input data.
    See the documentation for more information:

        https://docs.zenml.io/user-guide/advanced-guide/configure-steps-pipelines

    Args:
        dataset_inf: The inference dataset.

    Returns:
        The predictions as pandas series
    """
    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    pipeline_extra = get_step_context().pipeline_run.config.extra
    promoted_version = str(get_step_context().model_config._get_model_version().number)

    deployment_service = mlflow_model_registry_deployer_step.entrypoint(
        registry_model_name=pipeline_extra["mlflow_model_name"],
        registry_model_version=promoted_version,
        replace_existing=True,
    )
    predictions = deployment_service.predict(request=dataset_inf)
    predictions = pd.Series(predictions, name="predicted")
    deployment_service.deprovision(force=True)
    ### YOUR CODE ENDS HERE ###

    return predictions
