# coding=utf-8
import os
from jinja2 import Environment
from jinja2 import FileSystemLoader

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
