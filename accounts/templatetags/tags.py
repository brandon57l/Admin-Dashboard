from django import template

register = template.Library()

@register.filter
def check_group(user, group_name):
    group = user.groups.all()[0].name
    return True if group == group_name else False
