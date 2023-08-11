<!-- markdown-link-check-disable -->

# 0.42.1

This is the first release of E2E project template. It includes reworked
E2E example from the ZenML core library for future reuse as a template.

This template version is tested with ZenML core 0.42.1 and will support 
later version until newer template version is released.

This release has a limited Windows support, please log any issues with 
Windows OS as issues in the repository.

## New Features
* Copier template of E2E example with hyperparameter tuning, model version 
promotion and batch scoring on top of trained model.
* Example extended with capabilities to:
    * skip hyperparameter tuning
    * run simple latest promotion
    * skip drift detection
