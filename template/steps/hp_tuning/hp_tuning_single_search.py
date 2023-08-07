# {% include 'license_header' %}


from typing import Annotated, Any, Dict

import pandas as pd
from config import MetaConfig
from sklearn.metrics import accuracy_score
from sklearn.model_selection import RandomizedSearchCV
from utils.sklearn_materializer import ModelInfoMaterializer
from zenml import step
from zenml.logger import get_logger

logger = get_logger(__name__)


@step(output_materializers=ModelInfoMaterializer)
def hp_tuning_single_search(
    dataset_trn: pd.DataFrame,
    dataset_tst: pd.DataFrame,
    config_key: str,
    target: str,
) -> Annotated[Dict[str, Any], "best_model"]:
    """Evaluate a trained model.

    This is an example of a model hyperparameter tuning step that takes
    in train and test datasets to perform a randomized search for best model
    in configured space.

    This step is parameterized to configure the step independently of the step code,
    before running it in a pipeline. In this example, the step can be configured
    to use different input datasets and also have a flag to fall back to default
    model architecture. See the documentation for more information:

        https://docs.zenml.io/user-guide/advanced-guide/configure-steps-pipelines

    Args:
        dataset_trn: The train dataset.
        dataset_tst: The test dataset.
        config_key: Key of tuning config in MetaConfig class.
        target: Name of target columns in dataset.

    Returns:
        The best possible model parameters for given config.
    """
    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    model_config = MetaConfig.supported_models[config_key]
    model_class = model_config["class"]
    search_grid = model_config["search_grid"]

    X_trn = dataset_trn.drop(columns=[target])
    y_trn = dataset_trn[target]
    X_tst = dataset_tst.drop(columns=[target])
    y_tst = dataset_tst[target]
    logger.info("Running Hyperparameter tuning...")
    best_model = {"class": None, "params": None, "metric": -1}
    cv = RandomizedSearchCV(
        estimator=model_class(),
        param_distributions=search_grid,
        cv=3,
        n_jobs=-1,
        n_iter=10,
        random_state=42,
        scoring="accuracy",
    )
    cv.fit(X=X_trn, y=y_trn)
    y_pred = cv.predict(X_tst)
    score = accuracy_score(y_tst, y_pred)
    best_model["class"] = model_class
    best_model["params"] = cv.best_params_
    best_model["metric"] = score
    ### YOUR CODE ENDS HERE ###
    return best_model
