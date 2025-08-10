from django import template

register = template.Library()

@register.filter
def format_currency(value):
    """
    Formats an integer or decimal value with a dot as a thousands separator.
    e.g., 9999999 => 9.999.999
    """
    try:
        # Format the number with commas (default for int), then replace commas with dots
        return f"{int(value):,}".replace(",", ".")
    except (ValueError, TypeError):
        return value