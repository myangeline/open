# coding=utf-8
import web

from web.contrib.template import render_jinja
from conf import settings

__author__ = 'sunshine'

urls = (
    '/', 'Index',
    '/login', 'Login',
    '/manage', 'ManageBlog',
    '/manage/blog', 'ManageBlog',
    '/manage/category', 'ManageCategory',
    '/category/(\d+)', 'Category',
    '/blog/(\d+)', 'Blog'
)

app = web.application(urls, locals())

render = render_jinja('templates', encoding='utf-8')


class Index:
    """
    首页
    """
    def GET(self):
        return render.index(locals())


class Login:
    """
    登录页
    """
    def GET(self):
        return render.login(locals())


class ManageCategory:
    """
    类别管理页
    """
    def GET(self):
        return render.manage_category(locals())


class ManageBlog:
    """
    博客管理页
    """
    def GET(self):
        return render.manage_blog(locals())


class Category:
    def GET(self, category_id):
        print('category_id:', category_id)
        return render.category(locals())


class Blog:
    def GET(self, blog_id):
        print("blog:", blog_id)
        return render.blog(locals())



if __name__ == '__main__':
    web.config.debug = settings.debug
    app.run()
