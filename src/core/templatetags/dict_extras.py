from django import template
register = template.Library()

@register.filter
def get_item(d, key):
    """
    d = dict-like (ex: {id: 'P1', ...})
    key = int
    """
    try:
        return d.get(int(key)) or d.get(str(key))
    except Exception:
        return None
