from django import template

register = template.Library()


@register.filter
def get_rank(page):

    return (int(page)-1)*50
