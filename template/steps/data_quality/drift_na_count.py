{% include 'templates/license_header' %}


import json

from zenml import step


@step
def drift_na_count(report: str, na_drift_tolerance: float = 0.1) -> None:
    """Analyze the Evidently Report and raise RuntimeError on
    high deviation of NA count in 2 datasets.

    Args:
        report: generated Evidently JSON report.
        na_drift_tolerance: If number of NAs in current changed more than threshold
            percentage error will be raised.

    Raises:
        RuntimeError: significant drift in NA Count
    """
    result = json.loads(report)["metrics"][0]["result"]
    if result["reference"]["number_of_missing_values"] > 0 and (
        abs(
            result["reference"]["number_of_missing_values"]
            - result["current"]["number_of_missing_values"]
        )
        / result["reference"]["number_of_missing_values"]
        > na_drift_tolerance
    ):
        raise RuntimeError(
            "Number of NA values in scoring dataset is significantly different compared to train dataset."
        )
