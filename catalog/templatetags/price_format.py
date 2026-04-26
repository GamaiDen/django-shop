from django import template

register = template.Library()


@register.filter
def rub_format(value):
    try:
        value = float(value)
        return f"{value:,.2f}".replace(",", " ").replace(".", ",")
    except (ValueError, TypeError):
        return value
