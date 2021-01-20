from django import template

register = template.Library()


@register.filter(name='replace_separator')
def replace_separator(string, last_sep: str = ', ', new_sep: str = ' • ') -> str:
    return new_sep.join(string.split(last_sep))
