# coding=utf-8
import datetime
import web
from web.contrib.template import render_jinja

from conf import settings
from models.blog import Blogs
from models.category import Category
from utils.mongodbutils import MongodbUtil
from utils.templateutils import register
from utils.utils import get_session, render_markdown, md5, login_decorator


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
    '/blog/(.+)', 'Blog'
)

app = web.application(urls, locals())

# session
session = get_session(app)

render = render_jinja('templates', encoding='utf-8')

# 注册jinja2模板的自定义过滤器
register(render)

mu = MongodbUtil()


class Index:
    """
    首页
    """

    def GET(self):
        blogs = mu.get_blog()
        items = {}
        for blog in blogs:
            name = blog['category']
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
        return render.login(locals())

    def POST(self):
        args = web.input()
        username = args.get('username', None)
        password = args.get('password', None)
        if username and password:
            password = md5(password)
            user = mu.get_user(username, password)
            if user:
                # 登录成功保存客户端的session_id,如果关闭浏览器或者更换浏览器则session失效
                # 登录的功能没做好，可以在登录成功后生成一个token返回，客户端每次请求都要带上这个token，这样就比较好的控制
                session.login = web.cookies().webpy_session_id
                raise web.seeother('/manage')
        raise web.seeother('/login')


class ManageCategory:
    """
    类别管理页
    """

    @login_decorator
    def GET(self):
        categories = mu.get_category()
        return render.manage_category(locals())

    @login_decorator
    def POST(self):
        category_name = web.input().get('category_name', None)
        if category_name:
            category_name = category_name.strip()
        category_id = web.input().get('category_id', None)
        category = Category()
        if category_id:
            category.id = category_id
        if category_name:
            category.name = category_name
        category.create_time = datetime.datetime.now()
        mu.update_category(category)
        raise web.seeother('/manage/category')


class ManageCategoryEdit:
    """
    编辑类别(删除)
    """

    @login_decorator
    def GET(self):
        category_id = web.input().get('id', None)
        if category_id:
            mu.del_category(category_id)
        raise web.seeother('/manage/category')


class ManageBlogDelete:
    """
    删除文章
    """

    @login_decorator
    def GET(self):
        blog_id = web.input().get('id', None)
        if blog_id:
            mu.del_blog(blog_id)
        raise web.seeother('/manage')


class ManageBlog:
    """
    博客管理页
    """

    @login_decorator
    def GET(self):
        blogs = mu.get_blog()
        return render.manage_blog(locals())


class ManageBlogEdit:
    """
    编辑文章
    """

    @login_decorator
    def GET(self):
        blog_id = web.input().get("id", None)
        categories = mu.get_category()
        if blog_id:
            blog = mu.get_blog(blog_id)
        else:
            blog = None
        return render.manage_blog_edit(locals())

    @login_decorator
    def POST(self):
        args = web.input(content={})
        blog_id = args.get("id", None)
        category_id = args.get("category_id", None)
        title = args.get("title", None)
        summary = args.get("summary", None)
        blog = Blogs()
        if title:
            blog.title = title
        if summary:
            blog.summary = summary

        if category_id:
            category = mu.get_category(category_id)
            blog.category = category['name']
            blog.category_id = category_id

        if 'content' in args:
            source_content = args.content.file.read()
            blog.source_content = source_content
            content = render_markdown(source_content)
            html_content = unicode(content, 'utf-8')
            blog.html_content = html_content
        blog.create_time = datetime.datetime.now()
        if blog_id:
            blog.id = blog_id
            mu.update_blog(blog)
        else:
            mu.insert_blog(blog)
        raise web.seeother('/manage')


class Blog:
    """
    文章
    """

    def GET(self, blog_id):
        blog = mu.get_blog(blog_id)
        if 'html_content' in blog:
            content = blog['html_content']
        else:
            content = ''
        return render.blog(locals())


if __name__ == '__main__':
    web.config.debug = settings.debug
    app.run()
    # app.wsgifunc()
