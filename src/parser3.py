import pydot
G = pydot.Dot(graph_type='digraph')

i = 0

def createNode(s):
    global i
    global G
    #  p = pydot.Node(str(i), label=s)
    print('p = pydot.Node(str(' + repr(i) + '), label=\'%s\')' %s)
    print('G.add_node(p)')
    i += 1
    #  print("Added node " + repr(i) + " with label " + s)
    return i

def gen(p, s):
    global G
    p[0] = createNode(s)
    for i in range(1,len(p)):
        if (type(p[i]) != int):
            p[i] = str(p[i])
            p[i] = createNode(p[i])
        print('G.add_edge(pydot.Edge(str(' + repr(p[0]) + '), str(' + repr(p[i]) + ')))')

#!/usr/bin/env python2

import ply.lex as lex
import ply.yacc as yacc
from model import *

class MyLexer(object):

    keywords = ('this', 'class', 'void', 'super', 'extends', 'implements', 'enum', 'interface',
                'byte', 'short', 'int', 'long', 'char', 'float', 'double', 'boolean', 'null',
                'true', 'false',
                'final', 'public', 'protected', 'private', 'abstract', 'static', 'strictfp', 'transient', 'volatile',
                'synchronized', 'native',
                'throws', 'default',
                'instanceof',
                'if', 'else', 'while', 'for', 'switch', 'case', 'assert', 'do',
                'break', 'continue', 'return', 'throw', 'try', 'catch', 'finally', 'new',
                'package', 'import'
    )

    tokens = [
        'NAME',
        'NUM',
        'CHAR_LITERAL',
        'STRING_LITERAL',
        'LINE_COMMENT', 'BLOCK_COMMENT',

        'OR', 'AND',
        'EQ', 'NEQ', 'GTEQ', 'LTEQ',
        'LSHIFT', 'RSHIFT', 'RRSHIFT',

        'TIMES_ASSIGN', 'DIVIDE_ASSIGN', 'REMAINDER_ASSIGN',
        'PLUS_ASSIGN', 'MINUS_ASSIGN', 'LSHIFT_ASSIGN', 'RSHIFT_ASSIGN', 'RRSHIFT_ASSIGN',
        'AND_ASSIGN', 'OR_ASSIGN', 'XOR_ASSIGN',

        'PLUSPLUS', 'MINUSMINUS',

        'ELLIPSIS'
    ] + [k.upper() for k in keywords]
    literals = '()+-*/=?:,.^|&~!=[]{};<>@%'

    t_NUM = r'\.?[0-9][0-9eE_lLdDa-fA-F.xXpP]*'
    t_CHAR_LITERAL = r'\'([^\\\n]|(\\.))*?\''
    t_STRING_LITERAL = r'\"([^\\\n]|(\\.))*?\"'

    t_ignore_LINE_COMMENT = '//.*'

    def t_BLOCK_COMMENT(self, t):
        r'/\*(.|\n)*?\*/'
        t.lexer.lineno += t.value.count('\n')

    t_OR = r'\|\|'
    t_AND = '&&'

    t_EQ = '=='
    t_NEQ = '!='
    t_GTEQ = '>='
    t_LTEQ = '<='

    t_LSHIFT = '<<'
    t_RSHIFT = '>>'
    t_RRSHIFT = '>>>'

    t_TIMES_ASSIGN = r'\*='
    t_DIVIDE_ASSIGN = '/='
    t_REMAINDER_ASSIGN = '%='
    t_PLUS_ASSIGN = r'\+='
    t_MINUS_ASSIGN = '-='
    t_LSHIFT_ASSIGN = '<<='
    t_RSHIFT_ASSIGN = '>>='
    t_RRSHIFT_ASSIGN = '>>>='
    t_AND_ASSIGN = '&='
    t_OR_ASSIGN = r'\|='
    t_XOR_ASSIGN = '\^='

    t_PLUSPLUS = r'\+\+'
    t_MINUSMINUS = r'\-\-'

    t_ELLIPSIS = r'\.\.\.'

    t_ignore = ' \t\f'

    def t_NAME(self, t):
        '[A-Za-z_$][A-Za-z0-9_$]*'
        if t.value in MyLexer.keywords:
            t.type = t.value.upper()
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_newline2(self, t):
        r'(\r\n)+'
        t.lexer.lineno += len(t.value) / 2

    def t_error(self, t):
        print("Illegal character '{}' ({}) in line {}".format(t.value[0], hex(ord(t.value[0])), t.lexer.lineno))
        t.lexer.skip(1)

class ExpressionParser(object):

    def p_expression(self, p):
        '''expression : assignment_expression'''
        gen(p, 'expression')

    def p_expression_not_name(self, p):
        '''expression_not_name : assignment_expression_not_name'''
        gen(p, 'expression_not_name')

    def p_assignment_expression(self, p):
        '''assignment_expression : assignment
                                 | conditional_expression'''
        gen(p, 'assignment_expression')

    def p_assignment_expression_not_name(self, p):
        '''assignment_expression_not_name : assignment
                                          | conditional_expression_not_name'''
        gen(p, 'assignment_expression_not_name')

    def p_assignment(self, p):
        '''assignment : postfix_expression assignment_operator assignment_expression'''
        gen(p, 'assignment')

    def p_assignment_operator(self, p):
        '''assignment_operator : '='
                               | TIMES_ASSIGN
                               | DIVIDE_ASSIGN
                               | REMAINDER_ASSIGN
                               | PLUS_ASSIGN
                               | MINUS_ASSIGN
                               | LSHIFT_ASSIGN
                               | RSHIFT_ASSIGN
                               | RRSHIFT_ASSIGN
                               | AND_ASSIGN
                               | OR_ASSIGN
                               | XOR_ASSIGN'''
        gen(p, 'assignment_operator')

    def p_conditional_expression(self, p):
        '''conditional_expression : conditional_or_expression
                                  | conditional_or_expression '?' expression ':' conditional_expression'''
        gen(p, 'conditional_expression')

    def p_conditional_expression_not_name(self, p):
        '''conditional_expression_not_name : conditional_or_expression_not_name
                                           | conditional_or_expression_not_name '?' expression ':' conditional_expression
                                           | name '?' expression ':' conditional_expression'''
        gen(p, 'conditional_expression_not_name')

    def binop(self, p, ctor):
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ctor(p[2], p[1], p[3])

    def p_conditional_or_expression(self, p):
        '''conditional_or_expression : conditional_and_expression
                                     | conditional_or_expression OR conditional_and_expression'''
        gen(p, 'conditional_or_expression')

    def p_conditional_or_expression_not_name(self, p):
        '''conditional_or_expression_not_name : conditional_and_expression_not_name
                                              | conditional_or_expression_not_name OR conditional_and_expression
                                              | name OR conditional_and_expression'''
        gen(p, 'conditional_or_expression_not_name')

    def p_conditional_and_expression(self, p):
        '''conditional_and_expression : inclusive_or_expression
                                      | conditional_and_expression AND inclusive_or_expression'''
        gen(p, 'conditional_and_expression')

    def p_conditional_and_expression_not_name(self, p):
        '''conditional_and_expression_not_name : inclusive_or_expression_not_name
                                               | conditional_and_expression_not_name AND inclusive_or_expression
                                               | name AND inclusive_or_expression'''
        gen(p, 'conditional_and_expression_not_name')

    def p_inclusive_or_expression(self, p):
        '''inclusive_or_expression : exclusive_or_expression
                                   | inclusive_or_expression '|' exclusive_or_expression'''
        gen(p, 'inclusive_or_expression')

    def p_inclusive_or_expression_not_name(self, p):
        '''inclusive_or_expression_not_name : exclusive_or_expression_not_name
                                            | inclusive_or_expression_not_name '|' exclusive_or_expression
                                            | name '|' exclusive_or_expression'''
        gen(p, 'inclusive_or_expression_not_name')

    def p_exclusive_or_expression(self, p):
        '''exclusive_or_expression : and_expression
                                   | exclusive_or_expression '^' and_expression'''
        gen(p, 'exclusive_or_expression')

    def p_exclusive_or_expression_not_name(self, p):
        '''exclusive_or_expression_not_name : and_expression_not_name
                                            | exclusive_or_expression_not_name '^' and_expression
                                            | name '^' and_expression'''
        gen(p, 'exclusive_or_expression_not_name')

    def p_and_expression(self, p):
        '''and_expression : equality_expression
                          | and_expression '&' equality_expression'''
        gen(p, 'and_expression')

    def p_and_expression_not_name(self, p):
        '''and_expression_not_name : equality_expression_not_name
                                   | and_expression_not_name '&' equality_expression
                                   | name '&' equality_expression'''
        gen(p, 'and_expression_not_name')

    def p_equality_expression(self, p):
        '''equality_expression : instanceof_expression
                               | equality_expression EQ instanceof_expression
                               | equality_expression NEQ instanceof_expression'''
        gen(p, 'equality_expression')

    def p_equality_expression_not_name(self, p):
        '''equality_expression_not_name : instanceof_expression_not_name
                                        | equality_expression_not_name EQ instanceof_expression
                                        | name EQ instanceof_expression
                                        | equality_expression_not_name NEQ instanceof_expression
                                        | name NEQ instanceof_expression'''
        gen(p, 'equality_expression_not_name')

    def p_instanceof_expression(self, p):
        '''instanceof_expression : relational_expression
                                 | instanceof_expression INSTANCEOF reference_type'''
        gen(p, 'instanceof_expression')

    def p_instanceof_expression_not_name(self, p):
        '''instanceof_expression_not_name : relational_expression_not_name
                                          | name INSTANCEOF reference_type
                                          | instanceof_expression_not_name INSTANCEOF reference_type'''
        gen(p, 'instanceof_expression_not_name')

    def p_relational_expression(self, p):
        '''relational_expression : shift_expression
                                 | relational_expression '>' shift_expression
                                 | relational_expression '<' shift_expression
                                 | relational_expression GTEQ shift_expression
                                 | relational_expression LTEQ shift_expression'''
        gen(p, 'relational_expression')

    def p_relational_expression_not_name(self, p):
        '''relational_expression_not_name : shift_expression_not_name
                                          | shift_expression_not_name '<' shift_expression
                                          | name '<' shift_expression
                                          | shift_expression_not_name '>' shift_expression
                                          | name '>' shift_expression
                                          | shift_expression_not_name GTEQ shift_expression
                                          | name GTEQ shift_expression
                                          | shift_expression_not_name LTEQ shift_expression
                                          | name LTEQ shift_expression'''
        gen(p, 'relational_expression_not_name')

    def p_shift_expression(self, p):
        '''shift_expression : additive_expression
                            | shift_expression LSHIFT additive_expression
                            | shift_expression RSHIFT additive_expression
                            | shift_expression RRSHIFT additive_expression'''
        gen(p, 'shift_expression')

    def p_shift_expression_not_name(self, p):
        '''shift_expression_not_name : additive_expression_not_name
                                     | shift_expression_not_name LSHIFT additive_expression
                                     | name LSHIFT additive_expression
                                     | shift_expression_not_name RSHIFT additive_expression
                                     | name RSHIFT additive_expression
                                     | shift_expression_not_name RRSHIFT additive_expression
                                     | name RRSHIFT additive_expression'''
        gen(p, 'shift_expression_not_name')

    def p_additive_expression(self, p):
        '''additive_expression : multiplicative_expression
                               | additive_expression '+' multiplicative_expression
                               | additive_expression '-' multiplicative_expression'''
        gen(p, 'additive_expression')

    def p_additive_expression_not_name(self, p):
        '''additive_expression_not_name : multiplicative_expression_not_name
                                        | additive_expression_not_name '+' multiplicative_expression
                                        | name '+' multiplicative_expression
                                        | additive_expression_not_name '-' multiplicative_expression
                                        | name '-' multiplicative_expression'''
        gen(p, 'additive_expression_not_name')

    def p_multiplicative_expression(self, p):
        '''multiplicative_expression : unary_expression
                                     | multiplicative_expression '*' unary_expression
                                     | multiplicative_expression '/' unary_expression
                                     | multiplicative_expression '%' unary_expression'''
        gen(p, 'multiplicative_expression')

    def p_multiplicative_expression_not_name(self, p):
        '''multiplicative_expression_not_name : unary_expression_not_name
                                              | multiplicative_expression_not_name '*' unary_expression
                                              | name '*' unary_expression
                                              | multiplicative_expression_not_name '/' unary_expression
                                              | name '/' unary_expression
                                              | multiplicative_expression_not_name '%' unary_expression
                                              | name '%' unary_expression'''
        gen(p, 'multiplicative_expression_not_name')

    def p_unary_expression(self, p):
        '''unary_expression : pre_increment_expression
                            | pre_decrement_expression
                            | '+' unary_expression
                            | '-' unary_expression
                            | unary_expression_not_plus_minus'''
        gen(p, 'unary_expression')

    def p_unary_expression_not_name(self, p):
        '''unary_expression_not_name : pre_increment_expression
                                     | pre_decrement_expression
                                     | '+' unary_expression
                                     | '-' unary_expression
                                     | unary_expression_not_plus_minus_not_name'''
        gen(p, 'unary_expression_not_name')

    def p_pre_increment_expression(self, p):
        '''pre_increment_expression : PLUSPLUS unary_expression'''
        gen(p, 'pre_increment_expression')

    def p_pre_decrement_expression(self, p):
        '''pre_decrement_expression : MINUSMINUS unary_expression'''
        gen(p, 'pre_decrement_expression')

    def p_unary_expression_not_plus_minus(self, p):
        '''unary_expression_not_plus_minus : postfix_expression
                                           | '~' unary_expression
                                           | '!' unary_expression
                                           | cast_expression'''
        gen(p, 'unary_expression_not_plus_minus')

    def p_unary_expression_not_plus_minus_not_name(self, p):
        '''unary_expression_not_plus_minus_not_name : postfix_expression_not_name
                                                    | '~' unary_expression
                                                    | '!' unary_expression
                                                    | cast_expression'''
        gen(p, 'unary_expression_not_plus_minus_not_name')

    def p_postfix_expression(self, p):
        '''postfix_expression : primary
                              | name
                              | post_increment_expression
                              | post_decrement_expression'''
        gen(p, 'postfix_expression')

    def p_postfix_expression_not_name(self, p):
        '''postfix_expression_not_name : primary
                                       | post_increment_expression
                                       | post_decrement_expression'''
        gen(p, 'postfix_expression_not_name')

    def p_post_increment_expression(self, p):
        '''post_increment_expression : postfix_expression PLUSPLUS'''
        gen(p, 'post_increment_expression')

    def p_post_decrement_expression(self, p):
        '''post_decrement_expression : postfix_expression MINUSMINUS'''
        gen(p, 'post_decrement_expression')

    def p_primary(self, p):
        '''primary : primary_no_new_array
                   | array_creation_with_array_initializer
                   | array_creation_without_array_initializer'''
        gen(p, 'primary')

    def p_primary_no_new_array(self, p):
        '''primary_no_new_array : literal
                                | THIS
                                | class_instance_creation_expression
                                | field_access
                                | method_invocation
                                | array_access'''
        gen(p, 'primary_no_new_array')

    def p_primary_no_new_array2(self, p):
        '''primary_no_new_array : '(' name ')'
                                | '(' expression_not_name ')' '''
        gen(p, 'primary_no_new_array2')

    def p_primary_no_new_array3(self, p):
        '''primary_no_new_array : name '.' THIS
                                | name '.' SUPER'''
        gen(p, 'primary_no_new_array3')

    def p_primary_no_new_array4(self, p):
        '''primary_no_new_array : name '.' CLASS
                                | name dims '.' CLASS
                                | primitive_type dims '.' CLASS
                                | primitive_type '.' CLASS'''
        gen(p, 'primary_no_new_array4')

    def p_dims_opt(self, p):
        '''dims_opt : dims'''
        gen(p, 'dims_opt')

    def p_dims_opt2(self, p):
        '''dims_opt : empty'''
        gen(p, 'dims_opt2')

    def p_dims(self, p):
        '''dims : dims_loop'''
        gen(p, 'dims')

    def p_dims_loop(self, p):
        '''dims_loop : one_dim_loop
                     | dims_loop one_dim_loop'''
        gen(p, 'dims_loop')

    def p_one_dim_loop(self, p):
        '''one_dim_loop : '[' ']' '''
        gen(p, 'one_dim_loop')

    def p_cast_expression(self, p):
        '''cast_expression : '(' primitive_type dims_opt ')' unary_expression'''
        gen(p, 'cast_expression')

    def p_cast_expression2(self, p):
        '''cast_expression : '(' name type_arguments dims_opt ')' unary_expression_not_plus_minus'''
        gen(p, 'cast_expression2')

    def p_cast_expression3(self, p):
        '''cast_expression : '(' name type_arguments '.' class_or_interface_type dims_opt ')' unary_expression_not_plus_minus'''
        gen(p, 'cast_expression3')

    def p_cast_expression4(self, p):
        '''cast_expression : '(' name ')' unary_expression_not_plus_minus'''
        gen(p, 'cast_expression4')

    def p_cast_expression5(self, p):
        '''cast_expression : '(' name dims ')' unary_expression_not_plus_minus'''
        gen(p, 'cast_expression5')

class StatementParser(object):

    def p_block(self, p):
        '''block : '{' block_statements_opt '}' '''
        gen(p, 'block')

    def p_block_statements_opt(self, p):
        '''block_statements_opt : block_statements'''
        gen(p, 'block_statements_opt')

    def p_block_statements_opt2(self, p):
        '''block_statements_opt : empty'''
        gen(p, 'block_statements_opt2')

    def p_block_statements(self, p):
        '''block_statements : block_statement
                            | block_statements block_statement'''
        gen(p, 'block_statements')

    def p_block_statement(self, p):
        '''block_statement : local_variable_declaration_statement
                           | statement
                           | class_declaration
                           | interface_declaration
                           | annotation_type_declaration
                           | enum_declaration'''
        gen(p, 'block_statement')

    def p_local_variable_declaration_statement(self, p):
        '''local_variable_declaration_statement : local_variable_declaration ';' '''
        gen(p, 'local_variable_declaration_statement')

    def p_local_variable_declaration(self, p):
        '''local_variable_declaration : type variable_declarators'''
        gen(p, 'local_variable_declaration')

    def p_local_variable_declaration2(self, p):
        '''local_variable_declaration : modifiers type variable_declarators'''
        gen(p, 'local_variable_declaration2')

    def p_variable_declarators(self, p):
        '''variable_declarators : variable_declarator
                                | variable_declarators ',' variable_declarator'''
        gen(p, 'variable_declarators')

    def p_variable_declarator(self, p):
        '''variable_declarator : variable_declarator_id
                               | variable_declarator_id '=' variable_initializer'''
        gen(p, 'variable_declarator')

    def p_variable_declarator_id(self, p):
        '''variable_declarator_id : NAME dims_opt'''
        gen(p, 'variable_declarator_id')

    def p_variable_initializer(self, p):
        '''variable_initializer : expression
                                | array_initializer'''
        gen(p, 'variable_initializer')

    def p_statement(self, p):
        '''statement : statement_without_trailing_substatement
                     | labeled_statement
                     | if_then_statement
                     | if_then_else_statement
                     | while_statement
                     | for_statement
                     | enhanced_for_statement'''
        gen(p, 'statement')

    def p_statement_without_trailing_substatement(self, p):
        '''statement_without_trailing_substatement : block
                                                   | expression_statement
                                                   | assert_statement
                                                   | empty_statement
                                                   | switch_statement
                                                   | do_statement
                                                   | break_statement
                                                   | continue_statement
                                                   | return_statement
                                                   | synchronized_statement
                                                   | throw_statement
                                                   | try_statement
                                                   | try_statement_with_resources'''
        gen(p, 'statement_without_trailing_substatement')

    def p_expression_statement(self, p):
        '''expression_statement : statement_expression ';'
                                | explicit_constructor_invocation'''
        gen(p, 'expression_statement')

    def p_statement_expression(self, p):
        '''statement_expression : assignment
                                | pre_increment_expression
                                | pre_decrement_expression
                                | post_increment_expression
                                | post_decrement_expression
                                | method_invocation
                                | class_instance_creation_expression'''
        gen(p, 'statement_expression')

    def p_comma_opt(self, p):
        '''comma_opt : ','
                     | empty'''
        gen(p, 'comma_opt')

    def p_array_initializer(self, p):
        '''array_initializer : '{' comma_opt '}' '''
        gen(p, 'array_initializer')

    def p_array_initializer2(self, p):
        '''array_initializer : '{' variable_initializers '}'
                             | '{' variable_initializers ',' '}' '''
        gen(p, 'array_initializer2')

    def p_variable_initializers(self, p):
        '''variable_initializers : variable_initializer
                                 | variable_initializers ',' variable_initializer'''
        gen(p, 'variable_initializers')

    def p_method_invocation(self, p):
        '''method_invocation : NAME '(' argument_list_opt ')' '''
        gen(p, 'method_invocation')

    def p_method_invocation2(self, p):
        '''method_invocation : name '.' type_arguments NAME '(' argument_list_opt ')'
                             | primary '.' type_arguments NAME '(' argument_list_opt ')'
                             | SUPER '.' type_arguments NAME '(' argument_list_opt ')' '''
        gen(p, 'method_invocation2')

    def p_method_invocation3(self, p):
        '''method_invocation : name '.' NAME '(' argument_list_opt ')'
                             | primary '.' NAME '(' argument_list_opt ')'
                             | SUPER '.' NAME '(' argument_list_opt ')' '''
        gen(p, 'method_invocation3')

    def p_labeled_statement(self, p):
        '''labeled_statement : label ':' statement'''
        gen(p, 'labeled_statement')

    def p_labeled_statement_no_short_if(self, p):
        '''labeled_statement_no_short_if : label ':' statement_no_short_if'''
        gen(p, 'labeled_statement_no_short_if')

    def p_label(self, p):
        '''label : NAME'''
        gen(p, 'label')

    def p_if_then_statement(self, p):
        '''if_then_statement : IF '(' expression ')' statement'''
        gen(p, 'if_then_statement')

    def p_if_then_else_statement(self, p):
        '''if_then_else_statement : IF '(' expression ')' statement_no_short_if ELSE statement'''
        gen(p, 'if_then_else_statement')

    def p_if_then_else_statement_no_short_if(self, p):
        '''if_then_else_statement_no_short_if : IF '(' expression ')' statement_no_short_if ELSE statement_no_short_if'''
        gen(p, 'if_then_else_statement_no_short_if')

    def p_while_statement(self, p):
        '''while_statement : WHILE '(' expression ')' statement'''
        gen(p, 'while_statement')

    def p_while_statement_no_short_if(self, p):
        '''while_statement_no_short_if : WHILE '(' expression ')' statement_no_short_if'''
        gen(p, 'while_statement_no_short_if')

    def p_for_statement(self, p):
        '''for_statement : FOR '(' for_init_opt ';' expression_opt ';' for_update_opt ')' statement'''
        gen(p, 'for_statement')

    def p_for_statement_no_short_if(self, p):
        '''for_statement_no_short_if : FOR '(' for_init_opt ';' expression_opt ';' for_update_opt ')' statement_no_short_if'''
        gen(p, 'for_statement_no_short_if')

    def p_for_init_opt(self, p):
        '''for_init_opt : for_init
                        | empty'''
        gen(p, 'for_init_opt')

    def p_for_init(self, p):
        '''for_init : statement_expression_list
                    | local_variable_declaration'''
        gen(p, 'for_init')

    def p_statement_expression_list(self, p):
        '''statement_expression_list : statement_expression
                                     | statement_expression_list ',' statement_expression'''
        gen(p, 'statement_expression_list')

    def p_expression_opt(self, p):
        '''expression_opt : expression
                          | empty'''
        gen(p, 'expression_opt')

    def p_for_update_opt(self, p):
        '''for_update_opt : for_update
                          | empty'''
        gen(p, 'for_update_opt')

    def p_for_update(self, p):
        '''for_update : statement_expression_list'''
        gen(p, 'for_update')

    def p_enhanced_for_statement(self, p):
        '''enhanced_for_statement : enhanced_for_statement_header statement'''
        gen(p, 'enhanced_for_statement')

    def p_enhanced_for_statement_no_short_if(self, p):
        '''enhanced_for_statement_no_short_if : enhanced_for_statement_header statement_no_short_if'''
        gen(p, 'enhanced_for_statement_no_short_if')

    def p_enhanced_for_statement_header(self, p):
        '''enhanced_for_statement_header : enhanced_for_statement_header_init ':' expression ')' '''
        gen(p, 'enhanced_for_statement_header')

    def p_enhanced_for_statement_header_init(self, p):
        '''enhanced_for_statement_header_init : FOR '(' type NAME dims_opt'''
        gen(p, 'enhanced_for_statement_header_init')

    def p_enhanced_for_statement_header_init2(self, p):
        '''enhanced_for_statement_header_init : FOR '(' modifiers type NAME dims_opt'''
        gen(p, 'enhanced_for_statement_header_init2')

    def p_statement_no_short_if(self, p):
        '''statement_no_short_if : statement_without_trailing_substatement
                                 | labeled_statement_no_short_if
                                 | if_then_else_statement_no_short_if
                                 | while_statement_no_short_if
                                 | for_statement_no_short_if
                                 | enhanced_for_statement_no_short_if'''
        gen(p, 'statement_no_short_if')

    def p_assert_statement(self, p):
        '''assert_statement : ASSERT expression ';'
                            | ASSERT expression ':' expression ';' '''
        gen(p, 'assert_statement')

    def p_empty_statement(self, p):
        '''empty_statement : ';' '''
        gen(p, 'empty_statement')

    def p_switch_statement(self, p):
        '''switch_statement : SWITCH '(' expression ')' switch_block'''
        gen(p, 'switch_statement')

    def p_switch_block(self, p):
        '''switch_block : '{' '}' '''
        gen(p, 'switch_block')

    def p_switch_block2(self, p):
        '''switch_block : '{' switch_block_statements '}' '''
        gen(p, 'switch_block2')

    def p_switch_block3(self, p):
        '''switch_block : '{' switch_labels '}' '''
        gen(p, 'switch_block3')

    def p_switch_block4(self, p):
        '''switch_block : '{' switch_block_statements switch_labels '}' '''
        gen(p, 'switch_block4')

    def p_switch_block_statements(self, p):
        '''switch_block_statements : switch_block_statement
                                   | switch_block_statements switch_block_statement'''
        gen(p, 'switch_block_statements')

    def p_switch_block_statement(self, p):
        '''switch_block_statement : switch_labels block_statements'''
        gen(p, 'switch_block_statement')

    def p_switch_labels(self, p):
        '''switch_labels : switch_label
                         | switch_labels switch_label'''
        gen(p, 'switch_labels')

    def p_switch_label(self, p):
        '''switch_label : CASE constant_expression ':'
                        | DEFAULT ':' '''
        gen(p, 'switch_label')

    def p_constant_expression(self, p):
        '''constant_expression : expression'''
        gen(p, 'constant_expression')

    def p_do_statement(self, p):
        '''do_statement : DO statement WHILE '(' expression ')' ';' '''
        gen(p, 'do_statement')

    def p_break_statement(self, p):
        '''break_statement : BREAK ';'
                           | BREAK NAME ';' '''
        gen(p, 'break_statement')

    def p_continue_statement(self, p):
        '''continue_statement : CONTINUE ';'
                              | CONTINUE NAME ';' '''
        gen(p, 'continue_statement')

    def p_return_statement(self, p):
        '''return_statement : RETURN expression_opt ';' '''
        gen(p, 'return_statement')

    def p_synchronized_statement(self, p):
        '''synchronized_statement : SYNCHRONIZED '(' expression ')' block'''
        gen(p, 'synchronized_statement')

    def p_throw_statement(self, p):
        '''throw_statement : THROW expression ';' '''
        gen(p, 'throw_statement')

    def p_try_statement(self, p):
        '''try_statement : TRY try_block catches
                         | TRY try_block catches_opt finally'''
        gen(p, 'try_statement')

    def p_try_block(self, p):
        '''try_block : block'''
        gen(p, 'try_block')

    def p_catches(self, p):
        '''catches : catch_clause
                   | catches catch_clause'''
        gen(p, 'catches')

    def p_catches_opt(self, p):
        '''catches_opt : catches'''
        gen(p, 'catches_opt')

    def p_catches_opt2(self, p):
        '''catches_opt : empty'''
        gen(p, 'catches_opt2')

    def p_catch_clause(self, p):
        '''catch_clause : CATCH '(' catch_formal_parameter ')' block'''
        gen(p, 'catch_clause')

    def p_catch_formal_parameter(self, p):
        '''catch_formal_parameter : modifiers_opt catch_type variable_declarator_id'''
        gen(p, 'catch_formal_parameter')

    def p_catch_type(self, p):
        '''catch_type : union_type'''
        gen(p, 'catch_type')

    def p_union_type(self, p):
        '''union_type : type
                      | union_type '|' type'''
        gen(p, 'union_type')

    def p_try_statement_with_resources(self, p):
        '''try_statement_with_resources : TRY resource_specification try_block catches_opt
                                        | TRY resource_specification try_block catches_opt finally'''
        gen(p, 'try_statement_with_resources')

    def p_resource_specification(self, p):
        '''resource_specification : '(' resources semi_opt ')' '''
        gen(p, 'resource_specification')

    def p_semi_opt(self, p):
        '''semi_opt : ';'
                    | empty'''
        gen(p, 'semi_opt')

    def p_resources(self, p):
        '''resources : resource
                     | resources trailing_semicolon resource'''
        gen(p, 'resources')

    def p_trailing_semicolon(self, p):
        '''trailing_semicolon : ';' '''
        gen(p, 'trailing_semicolon')

    def p_resource(self, p):
        '''resource : type variable_declarator_id '=' variable_initializer'''
        gen(p, 'resource')

    def p_resource2(self, p):
        '''resource : modifiers type variable_declarator_id '=' variable_initializer'''
        gen(p, 'resource2')

    def p_finally(self, p):
        '''finally : FINALLY block'''
        gen(p, 'finally')

    def p_explicit_constructor_invocation(self, p):
        '''explicit_constructor_invocation : THIS '(' argument_list_opt ')' ';'
                                           | SUPER '(' argument_list_opt ')' ';' '''
        gen(p, 'explicit_constructor_invocation')

    def p_explicit_constructor_invocation2(self, p):
        '''explicit_constructor_invocation : type_arguments SUPER '(' argument_list_opt ')' ';'
                                           | type_arguments THIS '(' argument_list_opt ')' ';' '''
        gen(p, 'explicit_constructor_invocation2')

    def p_explicit_constructor_invocation3(self, p):
        '''explicit_constructor_invocation : primary '.' SUPER '(' argument_list_opt ')' ';'
                                           | name '.' SUPER '(' argument_list_opt ')' ';'
                                           | primary '.' THIS '(' argument_list_opt ')' ';'
                                           | name '.' THIS '(' argument_list_opt ')' ';' '''
        gen(p, 'explicit_constructor_invocation3')

    def p_explicit_constructor_invocation4(self, p):
        '''explicit_constructor_invocation : primary '.' type_arguments SUPER '(' argument_list_opt ')' ';'
                                           | name '.' type_arguments SUPER '(' argument_list_opt ')' ';'
                                           | primary '.' type_arguments THIS '(' argument_list_opt ')' ';'
                                           | name '.' type_arguments THIS '(' argument_list_opt ')' ';' '''
        gen(p, 'explicit_constructor_invocation4')

    def p_class_instance_creation_expression(self, p):
        '''class_instance_creation_expression : NEW type_arguments class_type '(' argument_list_opt ')' class_body_opt'''
        gen(p, 'class_instance_creation_expression')

    def p_class_instance_creation_expression2(self, p):
        '''class_instance_creation_expression : NEW class_type '(' argument_list_opt ')' class_body_opt'''
        gen(p, 'class_instance_creation_expression2')

    def p_class_instance_creation_expression3(self, p):
        '''class_instance_creation_expression : primary '.' NEW type_arguments class_type '(' argument_list_opt ')' class_body_opt'''
        gen(p, 'class_instance_creation_expression3')

    def p_class_instance_creation_expression4(self, p):
        '''class_instance_creation_expression : primary '.' NEW class_type '(' argument_list_opt ')' class_body_opt'''
        gen(p, 'class_instance_creation_expression4')

    def p_class_instance_creation_expression5(self, p):
        '''class_instance_creation_expression : class_instance_creation_expression_name NEW class_type '(' argument_list_opt ')' class_body_opt'''
        gen(p, 'class_instance_creation_expression5')

    def p_class_instance_creation_expression6(self, p):
        '''class_instance_creation_expression : class_instance_creation_expression_name NEW type_arguments class_type '(' argument_list_opt ')' class_body_opt'''
        gen(p, 'class_instance_creation_expression6')

    def p_class_instance_creation_expression_name(self, p):
        '''class_instance_creation_expression_name : name '.' '''
        gen(p, 'class_instance_creation_expression_name')

    def p_class_body_opt(self, p):
        '''class_body_opt : class_body
                          | empty'''
        gen(p, 'class_body_opt')

    def p_field_access(self, p):
        '''field_access : primary '.' NAME
                        | SUPER '.' NAME'''
        gen(p, 'field_access')

    def p_array_access(self, p):
        '''array_access : name '[' expression ']'
                        | primary_no_new_array '[' expression ']'
                        | array_creation_with_array_initializer '[' expression ']' '''
        gen(p, 'array_access')

    def p_array_creation_with_array_initializer(self, p):
        '''array_creation_with_array_initializer : NEW primitive_type dim_with_or_without_exprs array_initializer
                                                 | NEW class_or_interface_type dim_with_or_without_exprs array_initializer'''
        gen(p, 'array_creation_with_array_initializer')

    def p_dim_with_or_without_exprs(self, p):
        '''dim_with_or_without_exprs : dim_with_or_without_expr
                                     | dim_with_or_without_exprs dim_with_or_without_expr'''
        gen(p, 'dim_with_or_without_exprs')

    def p_dim_with_or_without_expr(self, p):
        '''dim_with_or_without_expr : '[' expression ']'
                                    | '[' ']' '''
        gen(p, 'dim_with_or_without_expr')

    def p_array_creation_without_array_initializer(self, p):
        '''array_creation_without_array_initializer : NEW primitive_type dim_with_or_without_exprs
                                                    | NEW class_or_interface_type dim_with_or_without_exprs'''
        gen(p, 'array_creation_without_array_initializer')

class NameParser(object):

    def p_name(self, p):
        '''name : simple_name
                | qualified_name'''
        gen(p, 'name')

    def p_simple_name(self, p):
        '''simple_name : NAME'''
        gen(p, 'simple_name')

    def p_qualified_name(self, p):
        '''qualified_name : name '.' simple_name'''
        gen(p, 'qualified_name')

class LiteralParser(object):

    def p_literal(self, p):
        '''literal : NUM
                   | CHAR_LITERAL
                   | STRING_LITERAL
                   | TRUE
                   | FALSE
                   | NULL'''
        gen(p, 'literal')

class TypeParser(object):

    def p_modifiers_opt(self, p):
        '''modifiers_opt : modifiers'''
        gen(p, 'modifiers_opt')

    def p_modifiers_opt2(self, p):
        '''modifiers_opt : empty'''
        gen(p, 'modifiers_opt2')

    def p_modifiers(self, p):
        '''modifiers : modifier
                     | modifiers modifier'''
        gen(p, 'modifiers')

    def p_modifier(self, p):
        '''modifier : PUBLIC
                    | PROTECTED
                    | PRIVATE
                    | STATIC
                    | ABSTRACT
                    | FINAL
                    | NATIVE
                    | SYNCHRONIZED
                    | TRANSIENT
                    | VOLATILE
                    | STRICTFP
                    | annotation'''
        gen(p, 'modifier')

    def p_type(self, p):
        '''type : primitive_type
                | reference_type'''
        gen(p, 'type')

    def p_primitive_type(self, p):
        '''primitive_type : BOOLEAN
                          | VOID
                          | BYTE
                          | SHORT
                          | INT
                          | LONG
                          | CHAR
                          | FLOAT
                          | DOUBLE'''
        gen(p, 'primitive_type')

    def p_reference_type(self, p):
        '''reference_type : class_or_interface_type
                          | array_type'''
        gen(p, 'reference_type')

    def p_class_or_interface_type(self, p):
        '''class_or_interface_type : class_or_interface
                                   | generic_type'''
        gen(p, 'class_or_interface_type')

    def p_class_type(self, p):
        '''class_type : class_or_interface_type'''
        gen(p, 'class_type')

    def p_class_or_interface(self, p):
        '''class_or_interface : name
                              | generic_type '.' name'''
        gen(p, 'class_or_interface')

    def p_generic_type(self, p):
        '''generic_type : class_or_interface type_arguments'''
        gen(p, 'generic_type')

    def p_generic_type2(self, p):
        '''generic_type : class_or_interface '<' '>' '''
        gen(p, 'generic_type2')

#    def p_array_type(self, p):
#        '''array_type : primitive_type dims
#                      | name dims
#                      | array_type_with_type_arguments_name dims
#                      | generic_type dims'''
#       gen(p, 'array_type')
#
#    def p_array_type_with_type_arguments_name(self, p):
#        '''array_type_with_type_arguments_name : generic_type '.' name'''
        gen(p, 'array_type_with_type_arguments_name')

    def p_array_type(self, p):
        '''array_type : primitive_type dims
                      | name dims'''
        gen(p, 'array_type')

    def p_array_type2(self, p):
        '''array_type : generic_type dims'''
        gen(p, 'array_type2')

    def p_array_type3(self, p):
        '''array_type : generic_type '.' name dims'''
        gen(p, 'array_type3')

    def p_type_arguments(self, p):
        '''type_arguments : '<' type_argument_list1'''
        gen(p, 'type_arguments')

    def p_type_argument_list1(self, p):
        '''type_argument_list1 : type_argument1
                               | type_argument_list ',' type_argument1'''
        gen(p, 'type_argument_list1')

    def p_type_argument_list(self, p):
        '''type_argument_list : type_argument
                              | type_argument_list ',' type_argument'''
        gen(p, 'type_argument_list')

    def p_type_argument(self, p):
        '''type_argument : reference_type
                         | wildcard'''
        gen(p, 'type_argument')

    def p_type_argument1(self, p):
        '''type_argument1 : reference_type1
                          | wildcard1'''
        gen(p, 'type_argument1')

    def p_reference_type1(self, p):
        '''reference_type1 : reference_type '>'
                           | class_or_interface '<' type_argument_list2'''
        gen(p, 'reference_type1')

    def p_type_argument_list2(self, p):
        '''type_argument_list2 : type_argument2
                               | type_argument_list ',' type_argument2'''
        gen(p, 'type_argument_list2')

    def p_type_argument2(self, p):
        '''type_argument2 : reference_type2
                          | wildcard2'''
        gen(p, 'type_argument2')

    def p_reference_type2(self, p):
        '''reference_type2 : reference_type RSHIFT
                           | class_or_interface '<' type_argument_list3'''
        gen(p, 'reference_type2')

    def p_type_argument_list3(self, p):
        '''type_argument_list3 : type_argument3
                               | type_argument_list ',' type_argument3'''
        gen(p, 'type_argument_list3')

    def p_type_argument3(self, p):
        '''type_argument3 : reference_type3
                          | wildcard3'''
        gen(p, 'type_argument3')

    def p_reference_type3(self, p):
        '''reference_type3 : reference_type RRSHIFT'''
        gen(p, 'reference_type3')

    def p_wildcard(self, p):
        '''wildcard : '?'
                    | '?' wildcard_bounds'''
        gen(p, 'wildcard')

    def p_wildcard_bounds(self, p):
        '''wildcard_bounds : EXTENDS reference_type
                           | SUPER reference_type'''
        gen(p, 'wildcard_bounds')

    def p_wildcard1(self, p):
        '''wildcard1 : '?' '>'
                     | '?' wildcard_bounds1'''
        gen(p, 'wildcard1')

    def p_wildcard_bounds1(self, p):
        '''wildcard_bounds1 : EXTENDS reference_type1
                            | SUPER reference_type1'''
        gen(p, 'wildcard_bounds1')

    def p_wildcard2(self, p):
        '''wildcard2 : '?' RSHIFT
                     | '?' wildcard_bounds2'''
        gen(p, 'wildcard2')

    def p_wildcard_bounds2(self, p):
        '''wildcard_bounds2 : EXTENDS reference_type2
                            | SUPER reference_type2'''
        gen(p, 'wildcard_bounds2')

    def p_wildcard3(self, p):
        '''wildcard3 : '?' RRSHIFT
                     | '?' wildcard_bounds3'''
        gen(p, 'wildcard3')

    def p_wildcard_bounds3(self, p):
        '''wildcard_bounds3 : EXTENDS reference_type3
                            | SUPER reference_type3'''
        gen(p, 'wildcard_bounds3')

    def p_type_parameter_header(self, p):
        '''type_parameter_header : NAME'''
        gen(p, 'type_parameter_header')

    def p_type_parameters(self, p):
        '''type_parameters : '<' type_parameter_list1'''
        gen(p, 'type_parameters')

    def p_type_parameter_list(self, p):
        '''type_parameter_list : type_parameter
                               | type_parameter_list ',' type_parameter'''
        gen(p, 'type_parameter_list')

    def p_type_parameter(self, p):
        '''type_parameter : type_parameter_header
                          | type_parameter_header EXTENDS reference_type
                          | type_parameter_header EXTENDS reference_type additional_bound_list'''
        gen(p, 'type_parameter')

    def p_additional_bound_list(self, p):
        '''additional_bound_list : additional_bound
                                 | additional_bound_list additional_bound'''
        gen(p, 'additional_bound_list')

    def p_additional_bound(self, p):
        '''additional_bound : '&' reference_type'''
        gen(p, 'additional_bound')

    def p_type_parameter_list1(self, p):
        '''type_parameter_list1 : type_parameter1
                                | type_parameter_list ',' type_parameter1'''
        gen(p, 'type_parameter_list1')

    def p_type_parameter1(self, p):
        '''type_parameter1 : type_parameter_header '>'
                           | type_parameter_header EXTENDS reference_type1
                           | type_parameter_header EXTENDS reference_type additional_bound_list1'''
        gen(p, 'type_parameter1')

    def p_additional_bound_list1(self, p):
        '''additional_bound_list1 : additional_bound1
                                  | additional_bound_list additional_bound1'''
        gen(p, 'additional_bound_list1')

    def p_additional_bound1(self, p):
        '''additional_bound1 : '&' reference_type1'''
        gen(p, 'additional_bound1')

class ClassParser(object):

    def p_type_declaration(self, p):
        '''type_declaration : class_declaration
                            | interface_declaration
                            | enum_declaration
                            | annotation_type_declaration'''
        gen(p, 'type_declaration')

    def p_type_declaration2(self, p):
        '''type_declaration : ';' '''
        gen(p, 'type_declaration2')

    def p_class_declaration(self, p):
        '''class_declaration : class_header class_body'''
        gen(p, 'class_declaration')

    def p_class_header(self, p):
        '''class_header : class_header_name class_header_extends_opt class_header_implements_opt'''
        gen(p, 'class_header')

    def p_class_header_name(self, p):
        '''class_header_name : class_header_name1 type_parameters
                             | class_header_name1'''
        gen(p, 'class_header_name')

    def p_class_header_name1(self, p):
        '''class_header_name1 : modifiers_opt CLASS NAME'''
        gen(p, 'class_header_name1')

    def p_class_header_extends_opt(self, p):
        '''class_header_extends_opt : class_header_extends
                                    | empty'''
        gen(p, 'class_header_extends_opt')

    def p_class_header_extends(self, p):
        '''class_header_extends : EXTENDS class_type'''
        gen(p, 'class_header_extends')

    def p_class_header_implements_opt(self, p):
        '''class_header_implements_opt : class_header_implements
                                       | empty'''
        gen(p, 'class_header_implements_opt')

    def p_class_header_implements(self, p):
        '''class_header_implements : IMPLEMENTS interface_type_list'''
        gen(p, 'class_header_implements')

    def p_interface_type_list(self, p):
        '''interface_type_list : interface_type
                               | interface_type_list ',' interface_type'''
        gen(p, 'interface_type_list')

    def p_interface_type(self, p):
        '''interface_type : class_or_interface_type'''
        gen(p, 'interface_type')

    def p_class_body(self, p):
        '''class_body : '{' class_body_declarations_opt '}' '''
        gen(p, 'class_body')

    def p_class_body_declarations_opt(self, p):
        '''class_body_declarations_opt : class_body_declarations'''
        gen(p, 'class_body_declarations_opt')

    def p_class_body_declarations_opt2(self, p):
        '''class_body_declarations_opt : empty'''
        gen(p, 'class_body_declarations_opt2')

    def p_class_body_declarations(self, p):
        '''class_body_declarations : class_body_declaration
                                   | class_body_declarations class_body_declaration'''
        gen(p, 'class_body_declarations')

    def p_class_body_declaration(self, p):
        '''class_body_declaration : class_member_declaration
                                  | static_initializer
                                  | constructor_declaration'''
        gen(p, 'class_body_declaration')

    def p_class_body_declaration2(self, p):
        '''class_body_declaration : block'''
        gen(p, 'class_body_declaration2')

    def p_class_member_declaration(self, p):
        '''class_member_declaration : field_declaration
                                    | class_declaration
                                    | method_declaration
                                    | interface_declaration
                                    | enum_declaration
                                    | annotation_type_declaration'''
        gen(p, 'class_member_declaration')

    def p_class_member_declaration2(self, p):
        '''class_member_declaration : ';' '''
        gen(p, 'class_member_declaration2')

    def p_field_declaration(self, p):
        '''field_declaration : modifiers_opt type variable_declarators ';' '''
        gen(p, 'field_declaration')

    def p_static_initializer(self, p):
        '''static_initializer : STATIC block'''
        gen(p, 'static_initializer')

    def p_constructor_declaration(self, p):
        '''constructor_declaration : constructor_header method_body'''
        gen(p, 'constructor_declaration')

    def p_constructor_header(self, p):
        '''constructor_header : constructor_header_name formal_parameter_list_opt ')' method_header_throws_clause_opt'''
        gen(p, 'constructor_header')

    def p_constructor_header_name(self, p):
        '''constructor_header_name : modifiers_opt type_parameters NAME '('
                                   | modifiers_opt NAME '(' '''
        gen(p, 'constructor_header_name')

    def p_formal_parameter_list_opt(self, p):
        '''formal_parameter_list_opt : formal_parameter_list'''
        gen(p, 'formal_parameter_list_opt')

    def p_formal_parameter_list_opt2(self, p):
        '''formal_parameter_list_opt : empty'''
        gen(p, 'formal_parameter_list_opt2')

    def p_formal_parameter_list(self, p):
        '''formal_parameter_list : formal_parameter
                                 | formal_parameter_list ',' formal_parameter'''
        gen(p, 'formal_parameter_list')

    def p_formal_parameter(self, p):
        '''formal_parameter : modifiers_opt type variable_declarator_id
                            | modifiers_opt type ELLIPSIS variable_declarator_id'''
        gen(p, 'formal_parameter')

    def p_method_header_throws_clause_opt(self, p):
        '''method_header_throws_clause_opt : method_header_throws_clause
                                           | empty'''
        gen(p, 'method_header_throws_clause_opt')

    def p_method_header_throws_clause(self, p):
        '''method_header_throws_clause : THROWS class_type_list'''
        gen(p, 'method_header_throws_clause')

    def p_class_type_list(self, p):
        '''class_type_list : class_type_elt
                           | class_type_list ',' class_type_elt'''
        gen(p, 'class_type_list')

    def p_class_type_elt(self, p):
        '''class_type_elt : class_type'''
        gen(p, 'class_type_elt')

    def p_method_body(self, p):
        '''method_body : '{' block_statements_opt '}' '''
        gen(p, 'method_body')

    def p_method_declaration(self, p):
        '''method_declaration : abstract_method_declaration
                              | method_header method_body'''
        gen(p, 'method_declaration')

    def p_abstract_method_declaration(self, p):
        '''abstract_method_declaration : method_header ';' '''
        gen(p, 'abstract_method_declaration')

    def p_method_header(self, p):
        '''method_header : method_header_name formal_parameter_list_opt ')' method_header_extended_dims method_header_throws_clause_opt'''
        gen(p, 'method_header')

    def p_method_header_name(self, p):
        '''method_header_name : modifiers_opt type_parameters type NAME '('
                              | modifiers_opt type NAME '(' '''
        gen(p, 'method_header_name')

    def p_method_header_extended_dims(self, p):
        '''method_header_extended_dims : dims_opt'''
        gen(p, 'method_header_extended_dims')

    def p_interface_declaration(self, p):
        '''interface_declaration : interface_header interface_body'''
        gen(p, 'interface_declaration')

    def p_interface_header(self, p):
        '''interface_header : interface_header_name interface_header_extends_opt'''
        gen(p, 'interface_header')

    def p_interface_header_name(self, p):
        '''interface_header_name : interface_header_name1 type_parameters
                                 | interface_header_name1'''
        gen(p, 'interface_header_name')

    def p_interface_header_name1(self, p):
        '''interface_header_name1 : modifiers_opt INTERFACE NAME'''
        gen(p, 'interface_header_name1')

    def p_interface_header_extends_opt(self, p):
        '''interface_header_extends_opt : interface_header_extends'''
        gen(p, 'interface_header_extends_opt')

    def p_interface_header_extends_opt2(self, p):
        '''interface_header_extends_opt : empty'''
        gen(p, 'interface_header_extends_opt2')

    def p_interface_header_extends(self, p):
        '''interface_header_extends : EXTENDS interface_type_list'''
        gen(p, 'interface_header_extends')

    def p_interface_body(self, p):
        '''interface_body : '{' interface_member_declarations_opt '}' '''
        gen(p, 'interface_body')

    def p_interface_member_declarations_opt(self, p):
        '''interface_member_declarations_opt : interface_member_declarations'''
        gen(p, 'interface_member_declarations_opt')

    def p_interface_member_declarations_opt2(self, p):
        '''interface_member_declarations_opt : empty'''
        gen(p, 'interface_member_declarations_opt2')

    def p_interface_member_declarations(self, p):
        '''interface_member_declarations : interface_member_declaration
                                         | interface_member_declarations interface_member_declaration'''
        gen(p, 'interface_member_declarations')

    def p_interface_member_declaration(self, p):
        '''interface_member_declaration : constant_declaration
                                        | abstract_method_declaration
                                        | class_declaration
                                        | interface_declaration
                                        | enum_declaration
                                        | annotation_type_declaration'''
        gen(p, 'interface_member_declaration')

    def p_interface_member_declaration2(self, p):
        '''interface_member_declaration : ';' '''
        gen(p, 'interface_member_declaration2')

    def p_constant_declaration(self, p):
        '''constant_declaration : field_declaration'''
        gen(p, 'constant_declaration')

    def p_enum_declaration(self, p):
        '''enum_declaration : enum_header enum_body'''
        gen(p, 'enum_declaration')

    def p_enum_header(self, p):
        '''enum_header : enum_header_name class_header_implements_opt'''
        gen(p, 'enum_header')

    def p_enum_header_name(self, p):
        '''enum_header_name : modifiers_opt ENUM NAME
                            | modifiers_opt ENUM NAME type_parameters'''
        gen(p, 'enum_header_name')

    def p_enum_body(self, p):
        '''enum_body : '{' enum_body_declarations_opt '}' '''
        gen(p, 'enum_body')

    def p_enum_body2(self, p):
        '''enum_body : '{' ',' enum_body_declarations_opt '}' '''
        gen(p, 'enum_body2')

    def p_enum_body3(self, p):
        '''enum_body : '{' enum_constants ',' enum_body_declarations_opt '}' '''
        gen(p, 'enum_body3')

    def p_enum_body4(self, p):
        '''enum_body : '{' enum_constants enum_body_declarations_opt '}' '''
        gen(p, 'enum_body4')

    def p_enum_constants(self, p):
        '''enum_constants : enum_constant
                          | enum_constants ',' enum_constant'''
        gen(p, 'enum_constants')

    def p_enum_constant(self, p):
        '''enum_constant : enum_constant_header class_body
                         | enum_constant_header'''
        gen(p, 'enum_constant')

    def p_enum_constant_header(self, p):
        '''enum_constant_header : enum_constant_header_name arguments_opt'''
        gen(p, 'enum_constant_header')

    def p_enum_constant_header_name(self, p):
        '''enum_constant_header_name : modifiers_opt NAME'''
        gen(p, 'enum_constant_header_name')

    def p_arguments_opt(self, p):
        '''arguments_opt : arguments'''
        gen(p, 'arguments_opt')

    def p_arguments_opt2(self, p):
        '''arguments_opt : empty'''
        gen(p, 'arguments_opt2')

    def p_arguments(self, p):
        '''arguments : '(' argument_list_opt ')' '''
        gen(p, 'arguments')

    def p_argument_list_opt(self, p):
        '''argument_list_opt : argument_list'''
        gen(p, 'argument_list_opt')

    def p_argument_list_opt2(self, p):
        '''argument_list_opt : empty'''
        gen(p, 'argument_list_opt2')

    def p_argument_list(self, p):
        '''argument_list : expression
                         | argument_list ',' expression'''
        gen(p, 'argument_list')

    def p_enum_body_declarations_opt(self, p):
        '''enum_body_declarations_opt : enum_declarations'''
        gen(p, 'enum_body_declarations_opt')

    def p_enum_body_declarations_opt2(self, p):
        '''enum_body_declarations_opt : empty'''
        gen(p, 'enum_body_declarations_opt2')

    def p_enum_body_declarations(self, p):
        '''enum_declarations : ';' class_body_declarations_opt'''
        gen(p, 'enum_body_declarations')

    def p_annotation_type_declaration(self, p):
        '''annotation_type_declaration : annotation_type_declaration_header annotation_type_body'''
        gen(p, 'annotation_type_declaration')

    def p_annotation_type_declaration_header(self, p):
        '''annotation_type_declaration_header : annotation_type_declaration_header_name class_header_extends_opt class_header_implements_opt'''
        gen(p, 'annotation_type_declaration_header')

    def p_annotation_type_declaration_header_name(self, p):
        '''annotation_type_declaration_header_name : modifiers '@' INTERFACE NAME'''
        gen(p, 'annotation_type_declaration_header_name')

    def p_annotation_type_declaration_header_name2(self, p):
        '''annotation_type_declaration_header_name : modifiers '@' INTERFACE NAME type_parameters'''
        gen(p, 'annotation_type_declaration_header_name2')

    def p_annotation_type_declaration_header_name3(self, p):
        '''annotation_type_declaration_header_name : '@' INTERFACE NAME type_parameters'''
        gen(p, 'annotation_type_declaration_header_name3')

    def p_annotation_type_declaration_header_name4(self, p):
        '''annotation_type_declaration_header_name : '@' INTERFACE NAME'''
        gen(p, 'annotation_type_declaration_header_name4')

    def p_annotation_type_body(self, p):
        '''annotation_type_body : '{' annotation_type_member_declarations_opt '}' '''
        gen(p, 'annotation_type_body')

    def p_annotation_type_member_declarations_opt(self, p):
        '''annotation_type_member_declarations_opt : annotation_type_member_declarations'''
        gen(p, 'annotation_type_member_declarations_opt')

    def p_annotation_type_member_declarations_opt2(self, p):
        '''annotation_type_member_declarations_opt : empty'''
        gen(p, 'annotation_type_member_declarations_opt2')

    def p_annotation_type_member_declarations(self, p):
        '''annotation_type_member_declarations : annotation_type_member_declaration
                                               | annotation_type_member_declarations annotation_type_member_declaration'''
        gen(p, 'annotation_type_member_declarations')

    def p_annotation_type_member_declaration(self, p):
        '''annotation_type_member_declaration : annotation_method_header ';'
                                              | constant_declaration
                                              | constructor_declaration
                                              | type_declaration'''
        gen(p, 'annotation_type_member_declaration')

    def p_annotation_method_header(self, p):
        '''annotation_method_header : annotation_method_header_name formal_parameter_list_opt ')' method_header_extended_dims annotation_method_header_default_value_opt'''
        gen(p, 'annotation_method_header')

    def p_annotation_method_header_name(self, p):
        '''annotation_method_header_name : modifiers_opt type_parameters type NAME '('
                                         | modifiers_opt type NAME '(' '''
        gen(p, 'annotation_method_header_name')

    def p_annotation_method_header_default_value_opt(self, p):
        '''annotation_method_header_default_value_opt : default_value
                                                      | empty'''
        gen(p, 'annotation_method_header_default_value_opt')

    def p_default_value(self, p):
        '''default_value : DEFAULT member_value'''
        gen(p, 'default_value')

    def p_member_value(self, p):
        '''member_value : conditional_expression_not_name
                        | name
                        | annotation
                        | member_value_array_initializer'''
        gen(p, 'member_value')

    def p_member_value_array_initializer(self, p):
        '''member_value_array_initializer : '{' member_values ',' '}'
                                          | '{' member_values '}' '''
        gen(p, 'member_value_array_initializer')

    def p_member_value_array_initializer2(self, p):
        '''member_value_array_initializer : '{' ',' '}'
                                          | '{' '}' '''
        gen(p, 'member_value_array_initializer2')

    def p_member_values(self, p):
        '''member_values : member_value
                         | member_values ',' member_value'''
        gen(p, 'member_values')

    def p_annotation(self, p):
        '''annotation : normal_annotation
                      | marker_annotation
                      | single_member_annotation'''
        gen(p, 'annotation')

    def p_normal_annotation(self, p):
        '''normal_annotation : annotation_name '(' member_value_pairs_opt ')' '''
        gen(p, 'normal_annotation')

    def p_annotation_name(self, p):
        '''annotation_name : '@' name'''
        gen(p, 'annotation_name')

    def p_member_value_pairs_opt(self, p):
        '''member_value_pairs_opt : member_value_pairs'''
        gen(p, 'member_value_pairs_opt')

    def p_member_value_pairs_opt2(self, p):
        '''member_value_pairs_opt : empty'''
        gen(p, 'member_value_pairs_opt2')

    def p_member_value_pairs(self, p):
        '''member_value_pairs : member_value_pair
                              | member_value_pairs ',' member_value_pair'''
        gen(p, 'member_value_pairs')

    def p_member_value_pair(self, p):
        '''member_value_pair : simple_name '=' member_value'''
        gen(p, 'member_value_pair')

    def p_marker_annotation(self, p):
        '''marker_annotation : annotation_name'''
        gen(p, 'marker_annotation')

    def p_single_member_annotation(self, p):
        '''single_member_annotation : annotation_name '(' single_member_annotation_member_value ')' '''
        gen(p, 'single_member_annotation')

    def p_single_member_annotation_member_value(self, p):
        '''single_member_annotation_member_value : member_value'''
        gen(p, 'single_member_annotation_member_value')

class CompilationUnitParser(object):

    def p_compilation_unit(self, p):
        '''compilation_unit : package_declaration'''
        gen(p, 'compilation_unit')

    def p_compilation_unit2(self, p):
        '''compilation_unit : package_declaration import_declarations'''
        gen(p, 'compilation_unit2')

    def p_compilation_unit3(self, p):
        '''compilation_unit : package_declaration import_declarations type_declarations'''
        gen(p, 'compilation_unit3')

    def p_compilation_unit4(self, p):
        '''compilation_unit : package_declaration type_declarations'''
        gen(p, 'compilation_unit4')

    def p_compilation_unit5(self, p):
        '''compilation_unit : import_declarations'''
        gen(p, 'compilation_unit5')

    def p_compilation_unit6(self, p):
        '''compilation_unit : type_declarations'''
        gen(p, 'compilation_unit6')

    def p_compilation_unit7(self, p):
        '''compilation_unit : import_declarations type_declarations'''
        gen(p, 'compilation_unit7')

    def p_compilation_unit8(self, p):
        '''compilation_unit : empty'''
        gen(p, 'compilation_unit8')

    def p_package_declaration(self, p):
        '''package_declaration : package_declaration_name ';' '''
        gen(p, 'package_declaration')

    def p_package_declaration_name(self, p):
        '''package_declaration_name : modifiers PACKAGE name
                                    | PACKAGE name'''
        gen(p, 'package_declaration_name')

    def p_import_declarations(self, p):
        '''import_declarations : import_declaration
                               | import_declarations import_declaration'''
        gen(p, 'import_declarations')

    def p_import_declaration(self, p):
        '''import_declaration : single_type_import_declaration
                              | type_import_on_demand_declaration
                              | single_static_import_declaration
                              | static_import_on_demand_declaration'''
        gen(p, 'import_declaration')

    def p_single_type_import_declaration(self, p):
        '''single_type_import_declaration : IMPORT name ';' '''
        gen(p, 'single_type_import_declaration')

    def p_type_import_on_demand_declaration(self, p):
        '''type_import_on_demand_declaration : IMPORT name '.' '*' ';' '''
        gen(p, 'type_import_on_demand_declaration')

    def p_single_static_import_declaration(self, p):
        '''single_static_import_declaration : IMPORT STATIC name ';' '''
        gen(p, 'single_static_import_declaration')

    def p_static_import_on_demand_declaration(self, p):
        '''static_import_on_demand_declaration : IMPORT STATIC name '.' '*' ';' '''
        gen(p, 'static_import_on_demand_declaration')

    def p_type_declarations(self, p):
        '''type_declarations : type_declaration
                             | type_declarations type_declaration'''
        gen(p, 'type_declarations')

class MyParser(ExpressionParser, NameParser, LiteralParser, TypeParser, ClassParser, StatementParser, CompilationUnitParser):

    tokens = MyLexer.tokens

    def p_goal_compilation_unit(self, p):
        '''goal : PLUSPLUS compilation_unit'''
        gen(p, 'goal_compilation_unit')
        gen(p, 'goal_compilation_unit')

    def p_goal_expression(self, p):
        '''goal : MINUSMINUS expression'''
        gen(p, 'goal_expression')

    def p_goal_statement(self, p):
        '''goal : '*' block_statement'''
        gen(p, 'goal_statement')

    def p_error(self, p):
        print('error: {}'.format(p))

    def p_empty(self, p):
        '''empty :'''

class Parser(object):

    def __init__(self):
        self.lexer = lex.lex(module=MyLexer(), optimize=1)
        self.parser = yacc.yacc(module=MyParser(), start='goal', optimize=1)

    def tokenize_string(self, code):
        self.lexer.input(code)
        for token in self.lexer:
            print(token)

    def tokenize_file(self, _file):
        if type(_file) == str:
            _file = open(_file)
        content = ''
        for line in _file:
            content += line
        return self.tokenize_string(content)

    def parse_expression(self, code, debug=0, lineno=1):
        return self.parse_string(code, debug, lineno, prefix='--')

    def parse_statement(self, code, debug=0, lineno=1):
        return self.parse_string(code, debug, lineno, prefix='* ')

    def parse_string(self, code, debug=0, lineno=1, prefix='++'):
        self.lexer.lineno = lineno
        return self.parser.parse(prefix + code, lexer=self.lexer, debug=debug)

    def parse_file(self, _file, debug=0):
        if type(_file) == str:
            _file = open(_file)
        content = _file.read()
        return self.parse_string(content, debug=debug)

if __name__ == '__main__':
    # for testing
    lexer = lex.lex(module=MyLexer())
    parser = yacc.yacc(module=MyParser(), write_tables=0, start='type_parameters')

    expressions = [
        '<T extends Foo & Bar>'
    ]

    for expr in expressions:
        print('lexing expression {}'.format(expr))
        lexer.input(expr)
        for token in lexer:
            print(token)

        print('parsing expression {}'.format(expr))
        t = parser.parse(expr, lexer=lexer, debug=1)
        print('result: {}'.format(t))
        print('--------------------------------')


#  p = createNode("Ayush")
#  q = createNode("Shivam")
#  graph.add_node(p)
#  graph.add_node(q)
#  graph.add_edge(pydot.Edge(p,q))
G.write_png('example1_graph.png')
