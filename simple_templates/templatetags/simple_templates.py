from urllib.parse import urlsplit, parse_qs, urlencode, urlunsplit

from django import template

register = template.Library()


@register.filter
def remove_query_param(url, param):
    url_parts = list(urlsplit(url))
    query = parse_qs(url_parts[3])

    query.pop(param, None)

    url_parts[3] = urlencode(query, doseq=True)
    return urlunsplit(url_parts)
