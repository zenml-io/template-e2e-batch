# {% include 'template/license_header' %}


from typing_extensions import Annotated

import pandas as pd
from zenml import step, get_step_context
from zenml.model import ArtifactConfig


@step
def inference_predict(
    dataset_inf: pd.DataFrame,
) -> Annotated[pd.Series, "predictions", ArtifactConfig(overwrite=False)]:
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
    model_version = get_step_context().model_config._get_model_version()

    # get predictor
    predictor = model_version.get_model_object("model").load()

    # run prediction and prepare output
    predictions = predictor.predict(dataset_inf)
    predictions = pd.Series(predictions, name="predicted")
    ### YOUR CODE ENDS HERE ###

    return predictions
