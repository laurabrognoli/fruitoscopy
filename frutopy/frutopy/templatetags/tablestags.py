from django import template
from ..choices import RIPENESS_CHOICES, FRUIT_CHOICES

register = template.Library()

@register.filter()
def getName(index):
    return FRUIT_CHOICES[index].capitalize()

@register.filter()
def getLabel(index):
    return RIPENESS_CHOICES[index][1].capitalize()