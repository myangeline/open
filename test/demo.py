# coding=utf-8
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.python import PythonLexer

__author__ = 'sunshine'

from pygments import highlight

code = 'print "Hello World"'
print highlight(code, PythonLexer(), HtmlFormatter())


def groupby(items, size):
    # print(a)
    # a = '123'
    print(list(iter(items)))
    print([iter(items)]*size)
    return zip(*[iter(items)]*size)


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
    C1().foo()
    C2().foo()
    pass