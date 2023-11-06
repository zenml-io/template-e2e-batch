# {% include 'template/license_header' %}


from typing import Optional
from typing_extensions import Annotated

from zenml import step, get_step_context
from zenml.client import Client
from zenml.logger import get_logger
from zenml.model import DeploymentArtifactConfig
from zenml.integrations.mlflow.steps.mlflow_deployer import (
    mlflow_model_registry_deployer_step,
)
from zenml.integrations.mlflow.services.mlflow_deployment import (
    MLFlowDeploymentService,
)
from utils import get_model_registry_version

logger = get_logger(__name__)


@step
def deployment_deploy() -> (
    Annotated[
        Optional[MLFlowDeploymentService],
        "mlflow_deployment",
        DeploymentArtifactConfig(),
    ]
):
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
    if Client().active_stack.orchestrator.flavor == "local":
        model_version = get_step_context().model_config._get_model_version()

        # deploy predictor service
        deployment_service = mlflow_model_registry_deployer_step.entrypoint(
            registry_model_name=model_version.model.name,
            registry_model_version=get_model_registry_version(model_version),
            replace_existing=True,
        )
    else:
        logger.warning("Skipping deployment as the orchestrator is not local.")
        deployment_service = None
    ### YOUR CODE ENDS HERE ###
    return deployment_service