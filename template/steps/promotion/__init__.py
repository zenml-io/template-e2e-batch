# {% include 'template/license_header' %}


{%- if metric_compare_promotion %}
from .compute_performance_metrics_on_current_data import compute_performance_metrics_on_current_data
from .promote_with_metric_compare import promote_with_metric_compare
{%- else %}
from .promote_latest_version import promote_latest_version
{%- endif %}
