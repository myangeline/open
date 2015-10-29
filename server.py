# coding=utf-8
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.python import PythonLexer
import requests

import web
from web.contrib.template import render_jinja

from conf import settings
from utils import markdown2
from utils.dbutils import get_category, add_category, delete_category, update_category, get_all_category, add_blog, \
    get_blog, delete_blog, get_blogs, update_blog
from utils.templateutils import register
from utils.utils import upload, get_session

__author__ = 'sunshine'

urls = (
    '/', 'Index',
    '/login', 'Login',
    '/manage', 'ManageBlog',
    '/manage/blog', 'ManageBlog',
    '/manage/blog/edit', 'ManageBlogEdit',
    '/manage/blog/delete', 'ManageBlogDelete',
    '/manage/category', 'ManageCategory',
    '/manage/category/edit', 'ManageCategoryEdit',
    '/blog/(\d+)', 'Blog',
    '/demo', 'Demo'
)

app = web.application(urls, locals())

# session
session = get_session(app)

render = render_jinja('templates', encoding='utf-8')

# 注册jinja2模板的自定义过滤器
register(render)


class Demo:
    def GET(self):
        with open(u'static/files/bottle笔记.md', 'r') as fh:
            content = fh.read()
            # content = highlight(content, PythonLexer(), HtmlFormatter())
            # print('=============================================================')
            # resp = requests.post('https://api.github.com/markdown/raw',
            #                      data=content,
            #                      headers={'content-type': 'text/plain'})
            # content = resp.text
            # content = highlight(content, PythonLexer(), HtmlFormatter())
            # print(content)
        # content = markdown2.markdown(content.decode('utf-8'), ['codehilite'])
        content = markdown2.markdown(content.decode('utf-8'))
        print(content)
        return render.demo(locals())


class Index:
    """
    首页
    """
    def GET(self):
        blogs = get_blogs()
        items = {}
        for blog in blogs:
            name = blog['name']
            if name in items:
                items[name].append(blog)
            else:
                items[name] = [blog]
        blogs = items
        return render.index(locals())


class Login:
    """
    登录页
    """
    def GET(self):
        session['name'] = 'admin'
        print(session['name'], session.name)
        print(session['count'])
        return render.login(locals())

    def POST(self):
        pass


class ManageCategory:
    """
    类别管理页
    """

    def GET(self):
        results = get_category()
        return render.manage_category(locals())

    def POST(self):
        category_name = web.input().get('category_name', None)
        if category_name:
            category_name = category_name.strip()
        category_id = web.input().get('category_id', None)
        if category_id and category_name:
            update_category(category_name, category_id)
        elif category_name:
            add_category(category_name, 1)
        raise web.seeother('/manage/category')


class ManageCategoryEdit:
    """
    编辑类别
    """

    def GET(self):
        category_id = web.input().get('id', None)
        if category_id:
            delete_category(category_id)
        raise web.seeother('/manage/category')


class ManageBlogDelete:
    """
    删除文章
    """

    def GET(self):
        blog_id = web.input().get('id', None)
        if blog_id:
            delete_blog(blog_id)
        raise web.seeother('/manage')


class ManageBlog:
    """
    博客管理页
    """

    def GET(self):
        blogs = get_blogs()
        return render.manage_blog(locals())


class ManageBlogEdit:
    """
    编辑文章
    """

    def GET(self):
        blog_id = web.input().get("id", None)
        categories = get_all_category()
        if blog_id:
            blog = get_blog(blog_id)
        else:
            blog = None
        return render.manage_blog_edit(locals())

    def POST(self):
        args = web.input(content={})
        blog_id = args.get("id", None)
        category_id = args.get("category_id", None)
        title = args.get("title", None)
        summary = args.get("summary", None)
        if 'content' in args:
            path = upload(args.content.filename, args.content.file)
        else:
            path = ""
        if blog_id:
            update_blog(title, summary, path, category_id, blog_id)
        else:
            add_blog(title, summary, path, category_id)
        raise web.seeother('/manage')


class Blog:
    """
    文章
    """
    def GET(self, blog_id):
        print("blog:", blog_id)
        blog = get_blog(blog_id)
        print(blog)
        # todo 每次去请求有点慢，可以存入数据库
        with open(blog['content'], 'r') as fh:
            content = fh.read()
            resp = requests.post('https://api.github.com/markdown/raw',
                                 data=content,
                                 headers={'content-type': 'text/plain'})
            content = resp.text
            # content = highlight(content, PythonLexer(), HtmlFormatter())
            print('content: ', content)
        return render.blog(locals())


if __name__ == '__main__':
    web.config.debug = settings.debug
    app.run()
