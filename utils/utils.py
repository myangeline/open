# coding=utf-8
import os
from jinja2 import Environment
from jinja2 import FileSystemLoader
import web
from conf import settings

__author__ = 'sunshine'


def render_template(template_name, **context):
    """
    jinja2配置渲染模板
    Example:

        >>> return render_template('hello.html', name='world',)
    :param template_name:
    :param context:
    :return:
    """
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
                            extensions=extensions, )
    jinja_env.globals.update(globals)

    # jinja_env.update_template_context(context)
    return jinja_env.get_template(template_name).render(context)


def upload(filename, f):
    """
    上传文件
    :param filename:
    :param f:
    :return:
    """
    file_path = filename.decode('utf-8').replace("\\", "/")
    file_name = file_path.split("/")[-1]
    path = os.path.join(settings.store_path, file_name)
    with open(path, 'w') as fh:
        fh.write(f.read())
    return path


def get_session(app):
    """
    获取session
    :param app:
    :return:
    """
    if web.config.get('_session') is None:
        session = web.session.Session(app, web.session.DiskStore('sessions'), {'count': 0})
        web.config._session = session
    else:
        session = web.config._session
    return session
