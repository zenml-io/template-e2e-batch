# {% include 'license_header' %}


{%- if metric_compare_promotion %}
from .promote_get_metric import promote_get_metric
from .promote_metric_compare_promoter import promote_metric_compare_promoter
{%- else %}
from .promote_latest import promote_latest
{%- endif %}
from .promote_get_versions import promote_get_versions
