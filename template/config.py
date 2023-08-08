# {% include 'license_header' %}


from artifacts.model_metadata import ModelMetadata
from pydantic import BaseConfig
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from zenml.config import DockerSettings
from zenml.integrations.constants import (
    AWS,
{%- if data_quality_checks %}
    EVIDENTLY,
{%- endif %}
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
{%- if data_quality_checks %}
            EVIDENTLY,
{%- endif %}
            KUBEFLOW,
            KUBERNETES,
            MLFLOW,
            SKLEARN,
            SLACK,
        ],
    )
)

DEFAULT_PIPELINE_EXTRAS = dict(
    notify_on_success={{notify_on_successes}}, 
    notify_on_failure={{notify_on_failures}}
)


class MetaConfig(BaseConfig):
    pipeline_name_training = "{{product_name}}_training"
    pipeline_name_batch_inference = "{{product_name}}_batch_inference"
    mlflow_model_name = "{{product_name}}_model"
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
