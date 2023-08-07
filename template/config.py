# {% include 'license_header' %}


from artifacts.model_metadata import ModelMetadata
from pydantic import BaseConfig
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from zenml.config import DockerSettings
from zenml.integrations.constants import (
    AWS,
    EVIDENTLY,
    KUBEFLOW,
    KUBERNETES,
    MLFLOW,
    SKLEARN,
    SLACK,
)
from zenml.model_registries.base_model_registry import ModelVersionStage

PIPELINE_SETTINGS = dict(
    docker=DockerSettings(
        required_integrations=[
            AWS,
            EVIDENTLY,
            KUBEFLOW,
            KUBERNETES,
            MLFLOW,
            SKLEARN,
            SLACK,
        ],
    )
)

DEFAULT_PIPELINE_EXTRAS = dict(notify_on_success=True, notify_on_failure=True)


class MetaConfig(BaseConfig):
    pipeline_name_training = "e2e_example_training"
    pipeline_name_batch_inference = "e2e_example_batch_inference"
    mlflow_model_name = "e2e_example_model"
    target_env = ModelVersionStage.STAGING
    supported_models = {
        "LogisticRegression": ModelMetadata(
            RandomForestClassifier,
            search_grid=dict(
                criterion=["gini", "entropy"],
                max_depth=[2, 4, 6, 8, 10, 12],
                min_samples_leaf=range(1, 10),
                n_estimators=range(50, 500, 25),
            ),
        ),
        "DecisionTreeClassifier": ModelMetadata(
            DecisionTreeClassifier,
            search_grid=dict(
                criterion=["gini", "entropy"],
                max_depth=[2, 4, 6, 8, 10, 12],
                min_samples_leaf=range(1, 10),
            ),
        ),
    }
    default_model_config = ModelMetadata(
        DecisionTreeClassifier,
        params=dict(
            criterion="gini",
            max_depth=5,
            min_samples_leaf=3,
        ),
    )
