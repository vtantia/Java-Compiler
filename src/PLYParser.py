import ply.lex as lex
import ply.yacc as yacc

# from model import *
from MyLexer import MyLexer
from MyParser import MyParser

class Parser(object):

    def __init__(self):
        self.lexer = lex.lex(module=MyLexer(), optimize=1)
        self.parserObj = MyParser(self.lexer)
        self.parser = yacc.yacc(module=self.parserObj, start='goal', optimize=1)

    def read_file(self, _file):
        if type(_file) == str:
            _file = open(_file)
        content = _file.read()
        _file.close()
        return content

    def tokenize_string(self, code):
        self.lexer.input(code)
        for token in self.lexer:
            print(token)

    def tokenize_file(self, _file):
        content = self.read_file(_file)
        return self.tokenize_string(content)

    def parse_expression(self, code, debug=0, lineno=1):
        return self.parse_string(code, debug, lineno, prefix='--')

    def parse_statement(self, code, debug=0, lineno=1):
        return self.parse_string(code, debug, lineno, prefix='* ')

    def parse_string(self, code, debug=0, lineno=1, prefix='++'):
        self.lexer.lineno = lineno
        return self.parser.parse(prefix + code, lexer=self.lexer, debug=debug)

    def parse_file(self, _file, debug=0):
        content = self.read_file(_file)
        parse_ret = self.parse_string(content, debug=debug)
        return parse_ret
