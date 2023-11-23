# {% include 'template/license_header' %}


from typing import Optional
from typing_extensions import Annotated

import pandas as pd
from zenml import get_step_context, step
from zenml.integrations.mlflow.services.mlflow_deployment import MLFlowDeploymentService
from zenml.logger import get_logger

logger = get_logger(__name__)


@step
def inference_predict(
    dataset_inf: pd.DataFrame,
) -> Annotated[pd.Series, "predictions"]:
    """Predictions step.

    This is an example of a predictions step that takes the data in and returns
    predicted values.

    This step is parameterized, which allows you to configure the step
    independently of the step code, before running it in a pipeline.
    In this example, the step can be configured to use different input data.
    See the documentation for more information:

        https://docs.zenml.io/user-guide/advanced-guide/configure-steps-pipelines

    Args:
        dataset_inf: The inference dataset.

    Returns:
        The predictions as pandas series
    """
    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    model_version = get_step_context().model_version

    # get predictor
    predictor_service: Optional[
        MLFlowDeploymentService
    ] = model_version.load_artifact("mlflow_deployment")
    if predictor_service is not None:
        # run prediction from service
        predictions = predictor_service.predict(request=dataset_inf)
    else:
        logger.warning(
            "Predicting from loaded model instead of deployment service "
            "as the orchestrator is not local."
        )
        # run prediction from memory
        predictor = model_version.load_artifact("model")
        predictions = predictor.predict(dataset_inf)

    predictions = pd.Series(predictions, name="predicted")
    ### YOUR CODE ENDS HERE ###

    return predictions
