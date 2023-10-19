# {% include 'template/license_header' %}


from typing_extensions import Annotated

from zenml import step, get_step_context
from zenml.client import Client
from zenml.logger import get_logger
from zenml.model_registries.base_model_registry import ModelVersionStage

logger = get_logger(__name__)

model_registry = Client().active_stack.model_registry


@step
def inference_get_current_version() -> Annotated[str, "model_version"]:
    """Get currently tagged model version for deployment.

    Returns:
        The model version of currently tagged model in Registry.
    """

    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    pipeline_extra = get_step_context().pipeline_run.config.extra
    current_version = model_registry.list_model_versions(
        name=pipeline_extra["mlflow_model_name"],
        stage=ModelVersionStage(pipeline_extra["target_env"]),
    )[0].version
    logger.info(
        f"Current model version in `{pipeline_extra['target_env']}` is `{current_version}`"
    )

    return current_version
