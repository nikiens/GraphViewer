import re

from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from antlr4.tree.Trees import Trees

from server.java.antlr.Java8Lexer import Java8Lexer
from server.java.antlr.Java8Parser import Java8Parser
from server.java.dot_gen.get_dot import get_dot


def get_ast(code):
    inp_stream = InputStream(code)
    lexer = Java8Lexer(inp_stream)
    lexer.removeErrorListeners()
    my_listener = MyErrorListener()
    lexer.addErrorListener(my_listener)
    stream = CommonTokenStream(lexer)
    parser = Java8Parser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(my_listener)
    tree = parser.compilationUnit()

    str_tree = Trees.toStringTree(tree, None, parser)

    sub = replace(r'\s\(\s*\)', str_tree, '')
    sub = replace(r'\s\(\s', sub, '')
    sub = replace(r'\"', sub, '\\"')

    return get_dot(sub)


def replace(regex, string, replacement):
    reg = re.compile(regex)
    return reg.sub(replacement, string)


class MyErrorListener(ErrorListener):

    def __init__(self):
        super(MyErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SyntaxError("line: {}, column: {}, msg: {}, e: {}".format(line, column, msg, e))
