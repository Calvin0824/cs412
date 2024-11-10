from django import template

register = template.Library()

@register.filter
def custom_range(value, end):
    """Generate a range from value to end."""
    return range(value, end + 1)