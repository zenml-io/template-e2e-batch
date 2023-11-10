# {% include 'template/license_header' %}

from steps import deployment_deploy,notify_on_success,notify_on_failure

from zenml import pipeline


@pipeline(on_failure=notify_on_failure)
def {{product_name}}_deployment():
    """
    Model deployment pipeline.

    This is a pipeline deploys trained model for future inference.
    """
    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    # Link all the steps together by calling them and passing the output
    # of one step as the input of the next step.
    ########## Deployment stage ##########
    deployment_deploy()

    notify_on_success(after=["deployment_deploy"])
    ### YOUR CODE ENDS HERE ###
