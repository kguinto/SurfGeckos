
from django import template
register = template.Library()


@register.simple_tag
def get_hazard(hazard_model, hazard_arg, site_value):
    hazard_value = getattr(hazard_model, hazard_arg)
    if site_value is not None and hazard_value is not None and site_value >= hazard_value:
        return "Yes"
    return ""
    