import datetime

__author__ = 'sunshine'


class Blog(object):
    id = None
    title = ""
    summary = ""
    html_content = ""
    source_content = ""
    category = "python"
    create_time = datetime.datetime.utcnow()
