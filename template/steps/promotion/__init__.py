# {% include 'template/license_header' %}


{%- if metric_compare_promotion %}
from .promote_get_metric import promote_get_metric
from .promote_metric_compare_promoter_in_model_registry import promote_metric_compare_promoter_in_model_registry
{%- else %}
from .promote_latest_in_model_registry import promote_latest_in_model_registry
{%- endif %}
from .promote_get_versions import promote_get_versions
from .promote_model_version_in_model_control_plane import promote_model_version_in_model_control_plane
