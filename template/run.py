# {% include 'template/license_header' %}

import click
from typing import Optional

from zenml.logger import get_logger

from main import main

logger = get_logger(__name__)


@click.command(
    help="""
{{ project_name }} CLI v{{ version }}.

Run the {{ project_name }} model training pipeline with various
options.

Examples:


\b
# Run the pipeline with default options
python run.py
            
\b
# Run the pipeline without cache
python run.py --no-cache

\b
# Run the pipeline without Hyperparameter tuning
python run.py --no-hp-tuning

\b
# Run the pipeline without NA drop and normalization, 
# but dropping columns [A,B,C] and keeping 10% of dataset 
# as test set.
python run.py --no-drop-na --no-normalize --drop-columns A,B,C --test-size 0.1

\b
# Run the pipeline with Quality Gate for accuracy set at 90% for train set 
# and 85% for test set. If any of accuracies will be lower - pipeline will fail.
python run.py --min-train-accuracy 0.9 --min-test-accuracy 0.85 --fail-on-accuracy-quality-gates


"""
)
@click.option(
    "--no-cache",
    is_flag=True,
    default=False,
    help="Disable caching for the pipeline run.",
)
@click.option(
    "--no-drop-na",
    is_flag=True,
    default=False,
    help="Whether to skip dropping rows with missing values in the dataset.",
)
@click.option(
    "--no-normalize",
    is_flag=True,
    default=False,
    help="Whether to skip normalization in the dataset.",
)
@click.option(
    "--drop-columns",
    default=None,
    type=click.STRING,
    help="Comma-separated list of columns to drop from the dataset.",
)
@click.option(
    "--test-size",
    default=0.2,
    type=click.FloatRange(0.0, 1.0),
    help="Proportion of the dataset to include in the test split.",
)
@click.option(
    "--min-train-accuracy",
    default=0.8,
    type=click.FloatRange(0.0, 1.0),
    help="Minimum training accuracy to pass to the model evaluator.",
)
@click.option(
    "--min-test-accuracy",
    default=0.8,
    type=click.FloatRange(0.0, 1.0),
    help="Minimum test accuracy to pass to the model evaluator.",
)
@click.option(
    "--fail-on-accuracy-quality-gates",
    is_flag=True,
    default=False,
    help="Whether to fail the pipeline run if the model evaluation step "
    "finds that the model is not accurate enough.",
)
@click.option(
    "--only-inference",
    is_flag=True,
    default=False,
    help="Whether to run only inference pipeline.",
)
def main_click(
    no_cache: bool = False,
    no_drop_na: bool = False,
    no_normalize: bool = False,
    drop_columns: Optional[str] = None,
    test_size: float = 0.2,
    min_train_accuracy: float = 0.8,
    min_test_accuracy: float = 0.8,
    fail_on_accuracy_quality_gates: bool = False,
    only_inference: bool = False,
):
    main(
        no_cache=no_cache,
        no_drop_na=no_drop_na,
        no_normalize=no_normalize,
        drop_columns=drop_columns,
        test_size=test_size,
        min_train_accuracy=min_train_accuracy,
        min_test_accuracy=min_test_accuracy,
        fail_on_accuracy_quality_gates=fail_on_accuracy_quality_gates,
        only_inference=only_inference,
    )


if __name__ == "__main__":
    main_click()
