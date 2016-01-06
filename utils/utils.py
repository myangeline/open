# coding=utf-8
import os
import re
import uuid
from jinja2 import Environment
from jinja2 import FileSystemLoader
import mistune
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.lexers.python import PythonLexer
import web
import hashlib
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
        session = web.session.Session(app, web.session.DiskStore('sessions'))
        web.config._session = session
    else:
        session = web.config._session

    def session_hook():
        web.ctx.session = session
        # 使session可以在模板中使用
        # web.template.Template.globals['session'] = session

    app.add_processor(web.loadhook(session_hook))

    return session


class HighlightRenderer(mistune.Renderer):
    """
    获取代码块，并做一些高亮的处理，可以直接使用pygments进行转换的操作
    暂时只能支持python的语法，其他的语言高亮还未做好

    现在可以支持
    ```lang
    code
    ```
    这样的语法，然后根据lang的语言名称获取pygments的对应的解析器，然后就可以解析出不同语言，
    设置对应的语法高亮
    """
    def block_code(self, code, lang):
        block_lexer = mistune.BlockLexer()
        m = re.match(block_lexer.grammar_class.fences, code)
        if m:
            lang = m.group(2)
            code = m.group(3)
        if not lang:
            code = highlight(code.decode('utf-8'), PythonLexer(), HtmlFormatter())
            return code.encode('utf-8')
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(code, lexer, formatter).encode('utf-8')


def render_markdown(code):
    """
    渲染markdown文档成html，并支持代码高亮
    :param code:
    :return:
    """
    renderer = HighlightRenderer()
    mk = mistune.Markdown(renderer=renderer)
    return mk(code)


def md5(text):
    """
    md5加密
    :param text:
    :return:
    """
    m = hashlib.md5()
    m.update(text)
    return m.hexdigest()


def get_token():
    """
    获取token值
    :return:
    """
    return str(uuid.uuid4())


def login_decorator(func):
    """
    登录装饰器
    :param func:
    :return:
    """
    def _wrapper(*args, **kwargs):
        if 'login' in web.ctx.session:
            if web.cookies().webpy_session_id == web.ctx.session.login:
                return func(*args, **kwargs)
        raise web.seeother('/login')
    return _wrapper


if __name__ == '__main__':
    # print(md5('jin@ll1314'))
    # print(get_token())
    doc = """
asasasasasa

    ```java
    System.out.println("Hello, Java!)
    ```
asasasas
"""
    md = render_markdown(doc)
    print(md)
    pass
