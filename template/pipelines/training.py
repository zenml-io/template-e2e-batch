# {% include 'template/license_header' %}


from typing import List, Optional

from artifacts.materializer import ModelMetadataMaterializer
from config import DEFAULT_PIPELINE_EXTRAS, PIPELINE_SETTINGS, MetaConfig
from steps import (
    data_loader,
{%- if hyperparameters_tuning %}
    hp_tuning_select_best_model,
    hp_tuning_single_search,
{%- endif %}
    model_evaluator,
    model_trainer,
    notify_on_failure,
    notify_on_success,
{%- if metric_compare_promotion %}
    promote_get_metric,
    promote_metric_compare_promoter,
{%- else %}
    promote_latest,
{%- endif %}
    promote_get_versions,
    train_data_preprocessor,
    train_data_splitter,
)
from zenml import pipeline
from zenml.integrations.mlflow.steps.mlflow_deployer import (
    mlflow_model_registry_deployer_step,
)
from zenml.integrations.mlflow.steps.mlflow_registry import mlflow_register_model_step
from zenml.logger import get_logger
from zenml.steps.external_artifact import ExternalArtifact


logger = get_logger(__name__)


@pipeline(
    settings=PIPELINE_SETTINGS,
    on_failure=notify_on_failure,
    extra=DEFAULT_PIPELINE_EXTRAS,
)
def {{product_name}}_training(
    test_size: float = 0.2,
    drop_na: Optional[bool] = None,
    normalize: Optional[bool] = None,
    drop_columns: Optional[List[str]] = None,
    random_seed: int = 42,
    min_train_accuracy: float = 0.0,
    min_test_accuracy: float = 0.0,
    fail_on_accuracy_quality_gates: bool = False,
):
    """
    Model training pipeline.

    This is a pipeline that loads the data, processes it and splits
    it into train and test sets, then search for best hyperparameters,
    trains and evaluates a model.

    Args:
        test_size: Size of holdout set for training 0.0..1.0
        drop_na: If `True` NA values will be removed from dataset
        normalize: If `True` dataset will be normalized with MinMaxScaler
        drop_columns: List of columns to drop from dataset
        random_seed: Seed of random generator,
        min_train_accuracy: Threshold to stop execution if train set accuracy is lower
        min_test_accuracy: Threshold to stop execution if test set accuracy is lower
        fail_on_accuracy_quality_gates: If `True` and `min_train_accuracy` or `min_test_accuracy`
            are not met - execution will be interrupted early

    """
    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    # Link all the steps together by calling them and passing the output
    # of one step as the input of the next step.
    ########## ETL stage ##########
    raw_data, target = data_loader()
    dataset_trn, dataset_tst = train_data_splitter(
        dataset=raw_data,
        test_size=test_size,
    )
    dataset_trn, dataset_tst, _ = train_data_preprocessor(
        dataset_trn=dataset_trn,
        dataset_tst=dataset_tst,
        drop_na=drop_na,
        normalize=normalize,
        drop_columns=drop_columns,
    )

{%- if hyperparameters_tuning %}
    ########## Hyperparameter tuning stage ##########
    after = []
    search_steps_prefix = "hp_tuning_search_"
    for i, model_search_configuration in enumerate(MetaConfig.model_search_space):
            step_name = f"{search_steps_prefix}{i}"
            hp_tuning_single_search(
                model_metadata=ExternalArtifact(
                    value=model_search_configuration,
                ),
                id=step_name,
                dataset_trn=dataset_trn,
                dataset_tst=dataset_tst,
                target=target,
            )
            after.append(step_name)
    best_model_config = hp_tuning_select_best_model(
        search_steps_prefix=search_steps_prefix, after=after
    )
{%- endif %}

    ########## Training stage ##########
    model = model_trainer(
        dataset_trn=dataset_trn,
{%- if hyperparameters_tuning %}
        model_config=best_model_config,
{%- else %}
        model_config=ExternalArtifact(value=MetaConfig.model_configuration, materializer=ModelMetadataMaterializer),
{%- endif %}
        random_seed=random_seed,
        target=target,
    )
    model_evaluator(
        model=model,
        dataset_trn=dataset_trn,
        dataset_tst=dataset_tst,
        min_train_accuracy=min_train_accuracy,
        min_test_accuracy=min_test_accuracy,
        fail_on_accuracy_quality_gates=fail_on_accuracy_quality_gates,
        target=target,
    )
    mlflow_register_model_step(
        model,
        name=MetaConfig.mlflow_model_name,
    )

    ########## Promotion stage ##########
    latest_version, current_version = promote_get_versions(
        after=["mlflow_register_model_step"],
    )
{%- if metric_compare_promotion %}
    latest_deployment = mlflow_model_registry_deployer_step(
        id="deploy_latest_model_version",
        registry_model_name=MetaConfig.mlflow_model_name,
        registry_model_version=latest_version,
        replace_existing=False,
    )
    latest_metric = promote_get_metric(
        id="get_metrics_latest_model_version",
        dataset_tst=dataset_tst,
        deployment_service=latest_deployment,
    )

    current_deployment = mlflow_model_registry_deployer_step(
        id="deploy_current_model_version",
        registry_model_name=MetaConfig.mlflow_model_name,
        registry_model_version=current_version,
        replace_existing=False,
        after=["get_metrics_latest_model_version"],
    )
    current_metric = promote_get_metric(
        id="get_metrics_current_model_version",
        dataset_tst=dataset_tst,
        deployment_service=current_deployment,
    )

    promote_metric_compare_promoter(
        latest_metric=latest_metric,
        current_metric=current_metric,
        latest_version=latest_version,
        current_version=current_version,
    )
    last_step_name = "promote_metric_compare_promoter"
{%- else %}
    promote_latest(
         latest_version=latest_version,
        current_version=current_version,
    )
    last_step_name = "promote_latest"
{%- endif %}

    notify_on_success(after=[last_step_name])
    ### YOUR CODE ENDS HERE ###
