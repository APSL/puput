# -*- coding: utf-8 -*-
from django.template import Library
from ..models import CustomCode

register = Library()

@register.inclusion_tag('puput/codes/custom_codes.html', takes_context=True)
def custom_codes(context):
    custom_codes = CustomCode.objects.filter(active=True)
    return {'custom_codes' : custom_codes}
