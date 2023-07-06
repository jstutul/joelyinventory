from django import template

register = template.Library()

@register.filter
def active_status(value):
    return "Active" if value.is_active else "Inactive"

@register.filter
def user_type(value):
    res="Sales"
    if value.is_staff:
        res="Inventory Department"
    if value.is_superuser and value.is_staff:
        res="Admin" 
                
    return res
