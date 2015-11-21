import datetime

__author__ = 'sunshine'


class Blogs(object):
    id = None
    title = ""
    summary = ""
    html_content = ""
    source_content = ""
    category = ""
    category_id = ""
    create_time = datetime.datetime.now()
