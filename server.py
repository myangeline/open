# coding=utf-8
import web
from web.contrib.template import render_jinja

from conf import settings
from utils.dbutils import get_category, add_category, delete_category, update_category, get_all_category, add_blog, \
    get_blog, delete_blog, get_blogs, update_blog, get_user
from utils.templateutils import register
from utils.utils import upload, get_session, render_markdown, md5, login_decorator


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
    '/blog/(\d+)', 'Blog'
)

app = web.application(urls, locals())

# session
session = get_session(app)

render = render_jinja('templates', encoding='utf-8')

# 注册jinja2模板的自定义过滤器
register(render)


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
        return render.login(locals())

    def POST(self):
        args = web.input()
        print(web.cookies().webpy_session_id)
        username = args.get('username', None)
        password = args.get('password', None)
        if username and password:
            password = md5(password)
            user = get_user(username, password)
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
        results = get_category()
        return render.manage_category(locals())

    @login_decorator
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
    @login_decorator
    def GET(self):
        blog_id = web.input().get('id', None)
        if blog_id:
            delete_blog(blog_id)
        raise web.seeother('/manage')


class ManageBlog:
    """
    博客管理页
    """
    @login_decorator
    def GET(self):
        blogs = get_blogs()
        return render.manage_blog(locals())


class ManageBlogEdit:
    """
    编辑文章
    """
    @login_decorator
    def GET(self):
        blog_id = web.input().get("id", None)
        categories = get_all_category()
        if blog_id:
            blog = get_blog(blog_id)
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
        with open(blog['content'], 'r') as fh:
            content = fh.read()
            content = render_markdown(content)
            content = unicode(content, 'utf-8')
        return render.blog(locals())


if __name__ == '__main__':
    web.config.debug = settings.debug
    app.run()
