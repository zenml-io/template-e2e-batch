# {% include 'template/license_header' %}


from typing import List, Optional
import random

from steps import (
    data_loader,
    model_evaluator,
    model_trainer,
    notify_on_failure,
    notify_on_success,
    train_data_preprocessor,
    train_data_splitter,
{%- if hyperparameters_tuning %}
    hp_tuning_select_best_model,
    hp_tuning_single_search,
{%- endif %}
{%- if metric_compare_promotion %}
    compute_performance_metrics_on_current_data,
    promote_with_metric_compare,
{%- else %}
    promote_latest_version,
{%- endif %}
)
from zenml import pipeline, get_pipeline_context
from zenml.logger import get_logger
{%- if hyperparameters_tuning %}

{%- else %}
from zenml.artifacts.external_artifact import ExternalArtifact

from utils import get_model_from_config
{%- endif %}

logger = get_logger(__name__)


@pipeline(on_failure=notify_on_failure)
def {{product_name}}_training(
    test_size: float = 0.2,
    drop_na: Optional[bool] = None,
    normalize: Optional[bool] = None,
    drop_columns: Optional[List[str]] = None,
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
        min_train_accuracy: Threshold to stop execution if train set accuracy is lower
        min_test_accuracy: Threshold to stop execution if test set accuracy is lower
        fail_on_accuracy_quality_gates: If `True` and `min_train_accuracy` or `min_test_accuracy`
            are not met - execution will be interrupted early

    """
    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    # Link all the steps together by calling them and passing the output
    # of one step as the input of the next step.
    pipeline_extra = get_pipeline_context().extra
    ########## ETL stage ##########
    raw_data, target, _ = data_loader(random_state=random.randint(0,100))
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
    for config_name,model_search_configuration in pipeline_extra["model_search_space"].items():
            step_name = f"{search_steps_prefix}{config_name}"
            hp_tuning_single_search(
                id=step_name,
                model_package = model_search_configuration["model_package"],
                model_class = model_search_configuration["model_class"],
                search_grid = model_search_configuration["search_grid"],
                dataset_trn=dataset_trn,
                dataset_tst=dataset_tst,
                target=target,
            )
            after.append(step_name)
    best_model = hp_tuning_select_best_model(after=after)
{%- else %}
    model_configuration = pipeline_extra["model_configuration"]
    best_model = get_model_from_config(
        model_package=model_configuration["model_package"], 
        model_class=model_configuration["model_class"],
        )(**model_configuration["params"])
{%- endif %}

    ########## Training stage ##########
    model = model_trainer(
        dataset_trn=dataset_trn,
{%- if hyperparameters_tuning %}
        model=best_model,
{%- else %}
        model=ExternalArtifact(value=best_model),
{%- endif %}
        target=target,
        name=pipeline_extra["mlflow_model_name"],
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
    ########## Promotion stage ##########
{%- if metric_compare_promotion %}
    latest_metric,current_metric = compute_performance_metrics_on_current_data(
        dataset_tst=dataset_tst,
        after=["model_evaluator"]
    )

    promote_with_metric_compare(
        latest_metric=latest_metric,
        current_metric=current_metric,
    )
    last_step = "promote_with_metric_compare"
{%- else %}
    promote_latest_version(after=["model_evaluator"])
    last_step = "promote_latest_version"
{%- endif %}

    notify_on_success(after=[last_step])
    ### YOUR CODE ENDS HERE ###
