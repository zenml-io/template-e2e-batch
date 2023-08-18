# {% include 'template/license_header' %}


from typing_extensions import Annotated

from config import MetaConfig
from zenml import step
from zenml.client import Client
from zenml.logger import get_logger

logger = get_logger(__name__)

model_registry = Client().active_stack.model_registry


@step
def inference_get_current_version() -> Annotated[str, "model_version"]:
    """Get currently tagged model version for deployment.

    Returns:
        The model version of currently tagged model in Registry.
    """

    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###

    current_version = model_registry.list_model_versions(
        name=MetaConfig.mlflow_model_name,
        metadata={},
        stage=MetaConfig.target_env,
    )[0].version
    logger.info(
        f"Current model version in `{MetaConfig.target_env.value}` is `{current_version}`"
    )

    return current_version
