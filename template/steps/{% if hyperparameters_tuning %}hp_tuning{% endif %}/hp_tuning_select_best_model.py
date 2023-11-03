# {% include 'template/license_header' %}


from typing_extensions import Annotated

from sklearn.base import ClassifierMixin

from zenml import get_step_context, step
from zenml.logger import get_logger

logger = get_logger(__name__)


@step
def hp_tuning_select_best_model() -> Annotated[ClassifierMixin, "best_model"]:
    """Find best model across all HP tuning attempts.

    This is an example of a model hyperparameter tuning step that loops 
    other artifacts linked to model version in Model Control Plane to find
    the best hyperparameter tuning output model of all according to the metric.

    Returns:
        The best possible model class and its' parameters.
    """
    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    model_version = get_step_context().model_config._get_model_version()

    best_model = None
    best_metric = -1
    # consume artifacts attached to current model version in Model Control Plane
    for full_artifact_name in model_version.artifact_object_ids:
        # if artifacts comes from one of HP tuning steps
        if full_artifact_name.endswith("hp_result"):
            hp_output = model_version.artifacts[full_artifact_name]["1"]
            model: ClassifierMixin = hp_output.load()
            # fetch metadata we attached earlier
            metric = float(hp_output.metadata["metric"].value)
            if best_model is None or best_metric < metric:
                best_model = model
    ### YOUR CODE ENDS HERE ###
    return best_model
