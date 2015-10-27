import web

from web.contrib.template import render_jinja
from conf import settings

__author__ = 'sunshine'

urls = (
    '/', 'Index'
)

app = web.application(urls, locals())

render = render_jinja('templates', encoding='utf-8')


class Index:
    def GET(self):
        name = "lujin"
        return render.index(locals())


class ManageCategory:
    def GET(self):
        return


if __name__ == '__main__':
    web.config.debug = settings.debug
    app.run()
