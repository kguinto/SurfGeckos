import re
from django import template
from django.conf import settings

numeric_test = re.compile("^\d+$")
register = template.Library()

@register.simple_tag
def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""

    if hasattr(value, str(arg)):
        value = getattr(value, arg)
        if type(value) == float:
            value = '%g' % value
        return value
    elif hasattr(value, 'has_key') and value.has_key(arg):
        return value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    else:
        return settings.TEMPLATE_STRING_IF_INVALID


@register.simple_tag
def general_number(value):

    if type(value) == float:
        value = '%g' % value
    return value