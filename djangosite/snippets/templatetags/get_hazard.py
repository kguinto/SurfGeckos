
from django import template
from . import getattribute

register = template.Library()


@register.simple_tag
def get_hazard(hazard_model, hazard_arg, site_value):
    return ""
    