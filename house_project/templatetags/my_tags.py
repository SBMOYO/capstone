from django import template

register = template.Library()

@register.filter
def first(queryset, house):
    return queryset.filter(house=house).first()
