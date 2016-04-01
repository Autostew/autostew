from datetime import timedelta

from django import template

from autostew.settings import dev
from autostew_back.utils import std_time_format


register = template.Library()

def is_missing(value):
    return value is None or value == dev.TEMPLATES[0]['OPTIONS']['string_if_invalid']

@register.filter
def milli_to_nicetime(value):
    if is_missing(value):
        return '---'
    return std_time_format(timedelta(milliseconds=value))


@register.filter
def temp(value):
    if is_missing(value):
        return 0
    return "{:.1f}".format(value/1000)


@register.filter
def pressure(value):
    if is_missing(value):
        return 0
    return "{:.0f}".format(value/100)


@register.filter
def percent(value):
    if is_missing(value):
        return 0
    return "{:.0f}".format(value/10)


@register.filter
def in_stage(value, stage):
    return value.filter(session_stage__name=stage)


@register.filter
def subtract(value, arg):
    return value - arg
