from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Dictionary'dan key bo'yicha qiymatni qaytaradi."""
    return dictionary.get(key, None)