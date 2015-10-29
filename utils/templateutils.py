__author__ = 'sunshine'


def register(render):
    environment = render._lookup
    environment.filters["format_str"] = format_str


def format_str(value, n=10):
    if len(value) > n:
        return value[:n]+'...'
    else:
        return value