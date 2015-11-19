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


if __name__ == '__main__':
    blog = Blog()
    print(blog.__class__.__dict__)
    pass

