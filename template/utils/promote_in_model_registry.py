# {% include 'template/license_header' %}


from zenml.client import Client
from zenml.logger import get_logger
from zenml.model_registries.base_model_registry import ModelVersionStage

logger = get_logger(__name__)


def promote_in_model_registry(
    latest_version: str, current_version: str, model_name: str, target_env: str
):
    model_registry = Client().active_stack.model_registry
    if latest_version != current_version:
        model_registry.update_model_version(
            name=model_name,
            version=current_version,
            stage=ModelVersionStage(ModelVersionStage.ARCHIVED),
            metadata={},
        )
    model_registry.update_model_version(
        name=model_name,
        version=latest_version,
        stage=ModelVersionStage(target_env),
        metadata={},
    )
