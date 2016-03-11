from datetime import timedelta

from django import template

from autostew_back.utils import std_time_format


register = template.Library()


@register.filter
def milli_to_nicetime(value):
    if value is None:
        return '---'
    return std_time_format(timedelta(milliseconds=value))


@register.filter
def temp(value):
    return "{:.1f}".format(value/1000)


@register.filter
def pressure(value):
    return "{:.0f}".format(value/100)


@register.filter
def percent(value):
    return "{:.0f}".format(value/10)
