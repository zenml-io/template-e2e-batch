{% include 'templates/license_header' %}


from typing import Annotated

import pandas as pd
from sklearn.metrics import accuracy_score

from zenml import step
from zenml.client import Client
from zenml.integrations.mlflow.services import MLFlowDeploymentService
from zenml.logger import get_logger

logger = get_logger(__name__)

model_registry = Client().active_stack.model_registry


@step
def promote_get_metric(
    dataset_tst: pd.DataFrame,
    deployment_service: MLFlowDeploymentService,
) -> Annotated[float, "metric"]:
    """Get metric for comparison for one model deployment.

    This is an example of a metric calculation step. It get a model deployment
    service and computes metric on recent test dataset.

    This step is parameterized, which allows you to configure the step
    independently of the step code, before running it in a pipeline.
    In this example, the step can be configured to use different input data.
    See the documentation for more information:

        https://docs.zenml.io/user-guide/advanced-guide/configure-steps-pipelines

    Args:
        dataset_tst: The test dataset.
        deployment_service: Model version deployment.

    Returns:
        Metric value for a given deployment on test set.

    """

    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    X = dataset_tst.drop(columns=["target"])
    y = dataset_tst["target"]
    logger.info("Evaluating model metrics...")

    predictions = deployment_service.predict(request=X)
    metric = accuracy_score(y, predictions)
    deployment_service.deprovision(force=True)
    ### YOUR CODE ENDS HERE ###
    return metric
