# {% include 'template/license_header' %}


from zenml import get_step_context, step
from zenml.logger import get_logger

logger = get_logger(__name__)


@step
def promote_model_version_in_model_control_plane(promotion_decision: bool):
    """Step to promote current model version to target environment in Model Control Plane.

    Args:
        promotion_decision: Whether to promote current model version to target environment
    """

    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    if promotion_decision:
        target_env = get_step_context().pipeline_run.config.extra["target_env"].lower()
        model_version = get_step_context().model_config._get_model_version()
        model_version.set_stage(stage=target_env, force=True)
        logger.info(f"Current model version was promoted to '{target_env}'.")
    else:
        logger.info("Current model version was not promoted.")
    ### YOUR CODE ENDS HERE ###
