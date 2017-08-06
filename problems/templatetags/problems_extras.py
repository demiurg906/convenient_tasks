import latex2mathml.converter
import logging
import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()
logger = logging.getLogger(__name__)


def convert_to_mathml(value):
    splitted = re.split(r'(\$.*?\$)', value)
    for i in range(1, len(splitted), 2):
        try:
            splitted[i] = latex2mathml.converter.convert(splitted[i][1:-1])
        except Exception as e:
            logger.exception(e)
            splitted[i] = f'<b><i>incorrect LaTeX input {splitted[i]}</i></b>'
    return ''.join(splitted)


@register.filter
def math(value):
    return mark_safe(convert_to_mathml(value))
