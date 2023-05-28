from django import template

register = template.Library()

@register.filter
def active_status(value):
    return "Active" if value.is_active else "Inactive"

@register.filter
def user_type(value):
    return "Admin" if value.is_staff else "Salesperson"
