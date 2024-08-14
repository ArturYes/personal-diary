from django import template


register = template.Library()


@register.filter
def media_url(data) -> str:
    if data:
        return f"/media/{data}"
    return "#"
