from MyLexer import MyLexer
from BaseParser import BaseParser
from OtherParsers import ExpressionParser, NameParser, LiteralParser, TypeParser, ClassParser, StatementParser, CompilationUnitParser

class MyParser(ExpressionParser, NameParser, LiteralParser, TypeParser, ClassParser, StatementParser, CompilationUnitParser):

    tokens = MyLexer.tokens
    def __init__(self, lexer):
        BaseParser.__init__(self)
        self.lexer = lexer

    def p_goal_compilation_unit(self, p):
        '''goal : PLUSPLUS compilation_unit'''
        # self.gen(p, 'goal')

    def p_goal_expression(self, p):
        '''goal : MINUSMINUS expression'''
        # self.gen(p, 'goal')

    def p_goal_statement(self, p):
        '''goal : '*' block_statement'''
        # self.gen(p, 'goal')

    def p_error(self, p):
        print('Error: \'{}\' at line no: {}'.format(p.value, p.lineno))
        with open(self.currFile, 'r') as fp:
            for i, line in enumerate(fp):
                if i+1 == p.lineno:
                    print(line)

    def p_empty(self, p):
        '''empty :'''
        # self.gen(p, 'empty')
