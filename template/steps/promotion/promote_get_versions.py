# {% include 'license_header' %}


from typing import Annotated, Tuple

from config import MetaConfig
from zenml import step
from zenml.client import Client
from zenml.logger import get_logger

logger = get_logger(__name__)

model_registry = Client().active_stack.model_registry


@step
def promote_get_versions() -> (
    Tuple[Annotated[str, "latest_version"], Annotated[str, "current_version"]]
):
    """Step to get latest and currently tagged model version from Model Registry.

    This is an example of a model version extraction step. It will retrieve 2 model
    versions from Model Registry: latest and currently promoted to target
    environment (Production, Staging, etc).

    Returns:
        The model versions: latest and current. If not current version - returns same
            for both.
    """

    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###

    none_versions = model_registry.list_model_versions(
        name=MetaConfig.mlflow_model_name,
        metadata={},
        stage=None,
    )
    latest_versions = none_versions[0].version
    logger.info(f"Latest model version is {latest_versions}")

    target_versions = model_registry.list_model_versions(
        name=MetaConfig.mlflow_model_name,
        metadata={},
        stage=MetaConfig.target_env,
    )
    current_version = latest_versions
    if target_versions:
        current_version = target_versions[0].version
        logger.info(f"Currently promoted model version is {current_version}")
    else:
        logger.info("No currently promoted model version found.")

    return latest_versions, current_version
