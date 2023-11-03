# {% include 'template/license_header' %}

from typing import Tuple
from typing_extensions import Annotated
from zenml.model import ModelConfig
from zenml.models.model_models import ModelVersionResponseModel


def _get_mr_version(model_version: ModelVersionResponseModel) -> str:
    """Read metadata of linked model object to fetch version in Model Registry.

    Args:
        model_version: Model Version response from Model Control Plane.
    """
    return (
        model_version.get_model_object("model").metadata["model_registry_version"].value
    )


def get_model_versions(
    model_version: ModelVersionResponseModel, target_env: str
) -> Tuple[Annotated[str, "latest_version"], Annotated[str, "current_version"]]:
    """Get latest and currently promoted model versions from Model Control Plane.

    Args:
        model_version: latest model version in Model Control Plane comming from context
        target_env: Target stage to search for currently promoted version
    """
    latest_version = _get_mr_version(model_version)
    try:
        current_model_version = ModelConfig(
            name=model_version.model.name, version=target_env
        )._get_model_version()
        current_version = _get_mr_version(current_model_version)
    except KeyError:
        current_version = latest_version

    return latest_version, current_version
