# {% include 'template/license_header' %}


from typing import Tuple
from typing_extensions import Annotated

import pandas as pd
from sklearn.datasets import load_breast_cancer
from zenml import step
from zenml.client import Client
from zenml.logger import get_logger

logger = get_logger(__name__)

artifact_store = Client().active_stack.artifact_store


@step
def data_loader(
    is_inference: bool = False,
) -> Tuple[Annotated[pd.DataFrame, "dataset"], Annotated[str, "target"],]:
    """Dataset reader step.

    This is an example of a dataset reader step that load Breast Cancer dataset.

    This step is parameterized, which allows you to configure the step
    independently of the step code, before running it in a pipeline.
    In this example, the step can be configured with number of rows and logic
    to drop target column or not. See the documentation for more information:

        https://docs.zenml.io/user-guide/advanced-guide/configure-steps-pipelines

    Args:
        is_inference: If `True` subset will be returned and target column
            will be removed from dataset.

    Returns:
        The dataset artifact as Pandas DataFrame and name of target column.
    """
    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    dataset = load_breast_cancer(as_frame=True)
    inference_size = int(len(dataset.target) * 0.05)
    target = "target"
    dataset: pd.DataFrame = dataset.frame
    inference_subset = dataset.sample(inference_size, random_state=42)
    if is_inference:
        dataset = inference_subset
        dataset.drop(columns=target, inplace=True)
    else:
        dataset.drop(inference_subset.index, inplace=True)
    dataset.reset_index(drop=True, inplace=True)
    logger.info(f"Dataset with {len(dataset)} records loaded!")
    ### YOUR CODE ENDS HERE ###
    return dataset, target
