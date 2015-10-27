from pygments.formatters.html import HtmlFormatter
from pygments.lexers.python import PythonLexer

__author__ = 'sunshine'

from pygments import highlight

code = 'print "Hello World"'
print highlight(code, PythonLexer(), HtmlFormatter())
