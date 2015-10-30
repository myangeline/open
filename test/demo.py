# coding=utf-8
import datetime
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.python import PythonLexer
import requests
import os

__author__ = 'sunshine'

from pygments import highlight

code = 'print "Hello World"'
print highlight(code, PythonLexer(), HtmlFormatter())


def groupby(items, size):
    # print(a)
    # a = '123'
    print(list(iter(items)))
    print([iter(items)] * size)
    return zip(*[iter(items)] * size)


# a = '123'


class A(object):
    def foo(self):
        print("A--foo()")


class B(object):
    def foo(self):
        print("B--foo()")


class P1(A):
    def foo(self):
        print("P1--foo()")

    pass


class P2(A):
    def foo(self):
        print("P2--foo()")

    def bar(self):
        print("P2--bar()")


class C1(P1, P2):
    pass


class C2(P2, P1):
    pass


if __name__ == '__main__':
    # print(groupby(range(9), 3))
    # MRO的算法有点小复杂，既不是深度优先，也不是广度优先
    """
    MRO算法有点坑
    """
    # C1().foo()
    # C2().foo()
    # blogs = [{u'created_at': datetime.datetime(2015, 10, 29, 16, 56, 51), u'summary': u'bottle\u7b14\u8bb0', u'id': 1, u'name': u'python', u'title': u'bottle\u7b14\u8bb0'}, {u'created_at': datetime.datetime(2015, 10, 29, 17, 1, 38), u'summary': u'1323sads', u'id': 2, u'name': u'php', u'title': u'centos\u5feb\u901f\u642d\u5efaftp\u670d\u52a1\u5668'}, {u'created_at': datetime.datetime(2015, 10, 29, 17, 0, 30), u'summary': u'centos\u5feb\u901f\u642d\u5efaftp\u670d\u52a1\u5668asasas', u'id': 3, u'name': u'java', u'title': u'centos\u5feb\u901f\u642d\u5efaftp\u670d\u52a1\u5668'}, {u'created_at': datetime.datetime(2015, 10, 29, 7, 3, 30), u'summary': u'aaaa', u'id': 4, u'name': u'python', u'title': u'abc'}, {u'created_at': datetime.datetime(2015, 10, 29, 7, 43, 14), u'summary': u'centos\u5feb\u901f\u642d\u5efaftp\u670d\u52a1\u5668', u'id': 6, u'name': u'python', u'title': u'centos\u5feb\u901f\u642d\u5efaftp\u670d\u52a1\u5668'}]
    # items = {}
    # for blog in blogs:
    # name = blog['name']
    #     if name in items:
    #         items[name].append(blog)
    #     else:
    #         items[name] = [blog]
    # print(items)
    # for item in items:
    #     print(item)
    # with open("G:/workspace/open/static/files/bottle笔记.md", 'r') as fh:
    #     content = fh.read()
    # headers = {'content-type': 'text/plain'}
    #
    # resp = requests.post('https://api.github.com/markdown/raw', data="Hello world github/linguist#1 **cool**, and #1!", headers={'content-type': 'text/plain'})
    # print(resp.text)
    content = """
        def get_db(db=db):
            conn = pymongo.Connection(host, port)
            conn.admin.authenticate(user, password)
            database = conn[db]
            return database
    """
    content = highlight(content, PythonLexer(), HtmlFormatter())
    print(content)
    pass