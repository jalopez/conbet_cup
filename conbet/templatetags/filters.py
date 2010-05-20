from django import template
from django.template.defaultfilters import stringfilter
import re

register = template.Library()

@register.filter
def hash(h, key):
    if key in h:
        return h[key]
    else:
        return None

@stringfilter
@register.filter
def sanitized(text):
    regexp = re.compile(r'\s*$', re.UNICODE)
    return re.sub(regexp, '', text)
