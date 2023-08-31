stack_name ?= e2e_template_stack

{%- if zenml_server_url != '' %}
remote-login:
	zenml connect --url "{{zenml_server_url}}"

setup: remote-login
{%- else %}
setup:
{%- endif %}
	pip install -r requirements.txt
	zenml integration install sklearn mlflow s3 kubernetes kubeflow slack evidently -y

install-stack:
	@echo "Specify stack name [$(stack_name)]: " && read input && [ -n "$$input" ] && stack_name="$$input" || stack_name="$(stack_name)" && \
	zenml experiment-tracker register -f mlflow mlflow_local_$${stack_name} && \
	zenml model-registry register -f mlflow mlflow_local_$${stack_name} && \
	zenml model-deployer register -f mlflow mlflow_local_$${stack_name} && \
	zenml data-validator register -f evidently evidently_$${stack_name} && \
	zenml stack register -a default -o default -r mlflow_local_$${stack_name} \
	-d mlflow_local_$${stack_name} -e mlflow_local_$${stack_name} -dv \
	evidently_$${stack_name} $${stack_name} && \
	zenml stack set $${stack_name} && \
	zenml stack up
