{%- if zenml_server_url != '' %}
remote-login:
	zenml connect --url "{{zenml_server_url}}"

setup: remote-login
{%- else %}
setup:
{%- endif %}
	pip install -r requirements.txt
	zenml up
	zenml integration install sklearn mlflow s3 kubernetes kubeflow slack evidently -y
# TODO: add stack configuration ^^^

