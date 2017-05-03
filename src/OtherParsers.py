from BaseParser import BaseParser
import re
import Node
from copy import deepcopy


class ExpressionParser(BaseParser):

    def p_expression(self, p):
        '''expression : assignment_expression'''
        self.gen(p, 'expression')

        self.tac.curTempCnt = 0
        p[0].temporary = self.tac.allotNewTemp()
        if p[1].temporary != p[0].temporary:
            self.tac.emit('move', p[1].temporary, p[0].temporary)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_expression_not_name(self, p):
        '''expression_not_name : assignment_expression_not_name'''
        self.gen(p, 'expression_not_name')

        self.tac.curTempCnt = 0
        p[0].temporary = self.tac.allotNewTemp()
        if p[1].temporary != p[0].temporary:
            self.tac.emit('move', p[1].temporary, p[0].temporary)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_assignment_expression(self, p):
        '''assignment_expression : assignment
                                 | conditional_expression'''
        self.gen(p, 'assignment_expression')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_assignment_expression_not_name(self, p):
        '''assignment_expression_not_name : assignment
                                          | conditional_expression_not_name'''
        self.gen(p, 'assignment_expression_not_name')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_assignment(self, p):
        '''assignment : postfix_expression assignment_operator assignment_expression'''
        self.gen(p, 'assignment', self.binary(p))
        p[0].nodeType = deepcopy(p[1].nodeType)
        self.assign(self.mapping[p[2].astName], p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

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
        self.gen(p, 'assignment_operator')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_conditional_expression(self, p):
        '''conditional_expression : conditional_or_expression
                                  | conditional_or_expression '?' expression ':' conditional_expression'''
        self.gen(p, 'conditional_expression')
        self.binary_exp_cond(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_conditional_expression_not_name(self, p):
        '''conditional_expression_not_name : conditional_or_expression_not_name
                                           | conditional_or_expression_not_name '?' expression ':' conditional_expression
                                           | name '?' expression ':' conditional_expression'''
        self.gen(p, 'conditional_expression_not_name')
        self.resolveScope(p[1])
        self.binary_exp_cond(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_conditional_or_expression(self, p):
        '''conditional_or_expression : conditional_and_expression
                                     | conditional_or_expression OR conditional_and_expression'''
        self.gen(p, 'conditional_or_expression', self.binary(p))
        self.binary_exp_bool(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_conditional_or_expression_not_name(self, p):
        '''conditional_or_expression_not_name : conditional_and_expression_not_name
                                              | conditional_or_expression_not_name OR conditional_and_expression
                                              | name OR conditional_and_expression'''
        self.gen(p, 'conditional_or_expression_not_name', self.binary(p))
        self.resolveScope(p[1])
        self.binary_exp_bool(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_conditional_and_expression(self, p):
        '''conditional_and_expression : inclusive_or_expression
                                      | conditional_and_expression AND inclusive_or_expression'''
        self.gen(p, 'conditional_and_expression', self.binary(p))
        self.binary_exp_bool(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_conditional_and_expression_not_name(self, p):
        '''conditional_and_expression_not_name : inclusive_or_expression_not_name
                                               | conditional_and_expression_not_name AND inclusive_or_expression
                                               | name AND inclusive_or_expression'''
        self.gen(p, 'conditional_and_expression_not_name', self.binary(p))
        self.resolveScope(p[1])
        self.binary_exp_bool(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_inclusive_or_expression(self, p):
        '''inclusive_or_expression : exclusive_or_expression
                                   | inclusive_or_expression '|' exclusive_or_expression'''
        self.gen(p, 'inclusive_or_expression', self.binary(p))
        self.binary_exp_bitwise(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_inclusive_or_expression_not_name(self, p):
        '''inclusive_or_expression_not_name : exclusive_or_expression_not_name
                                            | inclusive_or_expression_not_name '|' exclusive_or_expression
                                            | name '|' exclusive_or_expression'''
        self.gen(p, 'inclusive_or_expression_not_name', self.binary(p))
        self.resolveScope(p[1])
        self.binary_exp_bitwise(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_exclusive_or_expression(self, p):
        '''exclusive_or_expression : and_expression
                                   | exclusive_or_expression '^' and_expression'''
        self.gen(p, 'exclusive_or_expression', self.binary(p))
        self.binary_exp_bitwise(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_exclusive_or_expression_not_name(self, p):
        '''exclusive_or_expression_not_name : and_expression_not_name
                                            | exclusive_or_expression_not_name '^' and_expression
                                            | name '^' and_expression'''
        self.gen(p, 'exclusive_or_expression_not_name', self.binary(p))
        self.resolveScope(p[1])
        self.binary_exp_bitwise(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_and_expression(self, p):
        '''and_expression : equality_expression
                          | and_expression '&' equality_expression'''
        self.gen(p, 'and_expression', self.binary(p))
        self.binary_exp_bitwise(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_and_expression_not_name(self, p):
        '''and_expression_not_name : equality_expression_not_name
                                   | and_expression_not_name '&' equality_expression
                                   | name '&' equality_expression'''
        self.gen(p, 'and_expression_not_name', self.binary(p))
        self.resolveScope(p[1])
        self.binary_exp_bitwise(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_equality_expression(self, p):
        '''equality_expression : instanceof_expression
                               | equality_expression EQ instanceof_expression
                               | equality_expression NEQ instanceof_expression'''
        self.gen(p, 'equality_expression', self.binary(p))
        self.binary_exp_rel(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_equality_expression_not_name(self, p):
        '''equality_expression_not_name : instanceof_expression_not_name
                                        | equality_expression_not_name EQ instanceof_expression
                                        | name EQ instanceof_expression
                                        | equality_expression_not_name NEQ instanceof_expression
                                        | name NEQ instanceof_expression'''
        self.gen(p, 'equality_expression_not_name', self.binary(p))
        self.resolveScope(p[1])
        self.binary_exp_rel(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_instanceof_expression(self, p):
        '''instanceof_expression : relational_expression
                                 | instanceof_expression INSTANCEOF reference_type'''
        self.gen(p, 'instanceof_expression', self.binary(p))
        self.binary_exp_rel(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_instanceof_expression_not_name(self, p):
        '''instanceof_expression_not_name : relational_expression_not_name
                                          | name INSTANCEOF reference_type
                                          | instanceof_expression_not_name INSTANCEOF reference_type'''
        self.gen(p, 'instanceof_expression_not_name', self.binary(p))
        self.resolveScope(p[1])
        self.binary_exp_rel(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_relational_expression(self, p):
        '''relational_expression : shift_expression
                                 | relational_expression '>' shift_expression
                                 | relational_expression '<' shift_expression
                                 | relational_expression GTEQ shift_expression
                                 | relational_expression LTEQ shift_expression'''
        self.gen(p, 'relational_expression', self.binary(p))
        self.binary_exp_rel(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

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
        self.gen(p, 'relational_expression_not_name', self.binary(p))
        self.resolveScope(p[1])
        self.binary_exp_rel(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_shift_expression(self, p):
        '''shift_expression : additive_expression
                            | shift_expression LSHIFT additive_expression
                            | shift_expression RSHIFT additive_expression
                            | shift_expression RRSHIFT additive_expression'''
        self.gen(p, 'shift_expression', self.binary(p))
        self.binary_exp_shift(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_shift_expression_not_name(self, p):
        '''shift_expression_not_name : additive_expression_not_name
                                     | shift_expression_not_name LSHIFT additive_expression
                                     | name LSHIFT additive_expression
                                     | shift_expression_not_name RSHIFT additive_expression
                                     | name RSHIFT additive_expression
                                     | shift_expression_not_name RRSHIFT additive_expression
                                     | name RRSHIFT additive_expression'''
        self.gen(p, 'shift_expression_not_name', self.binary(p))
        self.resolveScope(p[1])
        self.binary_exp_shift(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_additive_expression(self, p):
        '''additive_expression : multiplicative_expression
                               | additive_expression '+' multiplicative_expression
                               | additive_expression '-' multiplicative_expression'''
        self.gen(p, 'additive_expression', self.binary(p))
        self.binary_exp_addmult(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_additive_expression_not_name(self, p):
        '''additive_expression_not_name : multiplicative_expression_not_name
                                        | additive_expression_not_name '+' multiplicative_expression
                                        | name '+' multiplicative_expression
                                        | additive_expression_not_name '-' multiplicative_expression
                                        | name '-' multiplicative_expression'''
        self.gen(p, 'additive_expression_not_name', self.binary(p))
        self.resolveScope(p[1])
        self.binary_exp_addmult(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_multiplicative_expression(self, p):
        '''multiplicative_expression : unary_expression
                                     | multiplicative_expression '*' unary_expression
                                     | multiplicative_expression '/' unary_expression
                                     | multiplicative_expression '%' unary_expression'''
        self.gen(p, 'multiplicative_expression', self.binary(p))
        self.binary_exp_addmult(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_multiplicative_expression_not_name(self, p):
        '''multiplicative_expression_not_name : unary_expression_not_name
                                              | multiplicative_expression_not_name '*' unary_expression
                                              | name '*' unary_expression
                                              | multiplicative_expression_not_name '/' unary_expression
                                              | name '/' unary_expression
                                              | multiplicative_expression_not_name '%' unary_expression
                                              | name '%' unary_expression'''
        self.gen(p, 'multiplicative_expression_not_name', self.binary(p))
        self.resolveScope(p[1])
        self.binary_exp_addmult(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_unary_expression(self, p):
        '''unary_expression : pre_increment_expression
                            | pre_decrement_expression
                            | '+' unary_expression
                            | '-' unary_expression
                            | unary_expression_not_plus_minus'''
        self.gen(p, 'unary_expression', self.unary(p))
        self.unary_exp_plus(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_unary_expression_not_name(self, p):
        '''unary_expression_not_name : pre_increment_expression
                                     | pre_decrement_expression
                                     | '+' unary_expression
                                     | '-' unary_expression
                                     | unary_expression_not_plus_minus_not_name'''
        self.gen(p, 'unary_expression_not_name', self.unary(p))
        self.unary_exp_plus(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_pre_increment_expression(self, p):
        '''pre_increment_expression : PLUSPLUS unary_expression'''
        self.gen(p, 'pre_increment_expression', self.unary(p))
        self.unary_exp_post(self, p, 2)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_pre_decrement_expression(self, p):
        '''pre_decrement_expression : MINUSMINUS unary_expression'''
        self.gen(p, 'pre_decrement_expression', self.unary(p))
        self.unary_exp_post(self, p, 2)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_unary_expression_not_plus_minus(self, p):
        '''unary_expression_not_plus_minus : postfix_expression
                                           | '~' unary_expression
                                           | '!' unary_expression
                                           | cast_expression'''
        self.gen(p, 'unary_expression_not_plus_minus', self.unary(p))
        self.unary_exp_nots(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_unary_expression_not_plus_minus_not_name(self, p):
        '''unary_expression_not_plus_minus_not_name : postfix_expression_not_name
                                                    | '~' unary_expression
                                                    | '!' unary_expression
                                                    | cast_expression'''
        self.gen(p, 'unary_expression_not_plus_minus_not_name', self.unary(p))
        self.unary_exp_nots(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_postfix_expression(self, p):
        '''postfix_expression : primary
                              | name
                              | post_increment_expression
                              | post_decrement_expression'''
        self.gen(p, 'postfix_expression')
        self.resolveScope(p[0])

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_postfix_expression_not_name(self, p):
        '''postfix_expression_not_name : primary
                                       | post_increment_expression
                                       | post_decrement_expression'''
        self.gen(p, 'postfix_expression_not_name')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_post_increment_expression(self, p):
        '''post_increment_expression : postfix_expression PLUSPLUS'''
        self.gen(p, 'post_increment_expression', 2)
        self.unary_exp_post(p, 1)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_post_decrement_expression(self, p):
        '''post_decrement_expression : postfix_expression MINUSMINUS'''
        self.gen(p, 'post_decrement_expression', 2)
        self.unary_exp_post(p, 1)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_primary(self, p):
        '''primary : primary_no_new_array
                   | array_creation_with_array_initializer
                   | array_creation_without_array_initializer'''
        self.gen(p, 'primary')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_primary_no_new_array(self, p):
        '''primary_no_new_array : literal
                                | THIS
                                | class_instance_creation_expression
                                | field_access
                                | method_invocation
                                | array_access'''
        self.gen(p, 'primary_no_new_array')
        if p[0].astName == 'this':
            for scope in reversed(self.symTabStack):
                if scope.get('desc') == 'class':
                    p[0].nodeType = Node.Type(baseType=scope['scope_name'])
                    break
            else:
                print('Something is wrong with the symbol table at lineno #{}'.
                        format(self.lexer.lineno))

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_primary_no_new_array2(self, p):
        '''primary_no_new_array : '(' name ')'
                                | '(' expression_not_name ')' '''
        self.gen(p, 'primary_no_new_array')
        self.resolveScope(p[2])
        p[0].nodeType = deepcopy(p[2].nodeType)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_dims_opt(self, p):
        '''dims_opt : dims'''
        self.gen(p, 'dims_opt')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_dims_opt2(self, p):
        '''dims_opt : empty'''
        self.gen(p, 'dims_opt')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_dims(self, p):
        '''dims : dims_loop'''
        self.gen(p, 'dims')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_dims_loop(self, p):
        '''dims_loop : one_dim_loop
                     | dims_loop one_dim_loop'''
        self.gen(p, 'dims_loop')
        if len(p) == 3:
            p[0].nodeType.dim = p[1].nodeType.dim + p[2].nodeType.dim

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_one_dim_loop(self, p):
        '''one_dim_loop : '[' ']' '''
        self.gen(p, 'one_dim_loop')
        p[0].nodeType.dim = [0]

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_cast_expression(self, p):
        '''cast_expression : '(' primitive_type dims_opt ')' unary_expression'''
        self.gen(p, 'cast_expression')
        p[0].nodeType.baseType = p[2].nodeType.baseType
        if p[3]:
            p[0].nodeType.dim = p[3].nodeType.dim

        if not self.checkTypeAssignment(p[0], p[5]):
            print('Can\'t cast the the paramter on line #{} to {}'.format(
                self.lexer.lineno, p[2].nodeType.baseType))

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()


class StatementParser(BaseParser):

    def p_M(self, p):
        ''' M : empty '''
        p[0] = self.makeMarkerNode()
        p[0].codeEnd = self.tac.nextquad()

    def p_N(self, p):
        ''' N : empty '''
        p[0] = self.makeMarkerNode()
        p[0].tacLists.nextList = [self.tac.nextquad()]
        self.tac.emit('JMP')

        p[0].codeEnd = self.tac.nextquad()

    def p_block(self, p):
        ''' block : '{' seen_Lbrace block_statements_opt '}' '''
        self.gen(p, 'block')
        self.endCurrScope()

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_seen_Lbrace(self, p):
        '''seen_Lbrace : empty'''
        self.appendNewScope('block')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_block_statements_opt(self, p):
        '''block_statements_opt : block_statements'''
        self.gen(p, 'block_statements_opt')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_block_statements_opt2(self, p):
        '''block_statements_opt : empty'''
        self.gen(p, 'block_statements_opt')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_block_statements(self, p):
        '''block_statements : block_statement
                            | block_statements block_statement'''
        self.gen(p, 'block_statements')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_block_statement(self, p):
        '''block_statement : local_variable_declaration_statement
                           | statement '''
        self.gen(p, 'block_statement')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_local_variable_declaration_statement(self, p):
        '''local_variable_declaration_statement : local_variable_declaration ';' '''
        self.gen(p, 'local_variable_declaration_statement')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_local_variable_declaration(self, p):
        '''local_variable_declaration : type variable_declarators'''
        self.gen(p, 'local_variable_declaration')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_local_variable_declaration2(self, p):
        '''local_variable_declaration : modifiers type variable_declarators'''
        self.gen(p, 'local_variable_declaration')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_variable_declarators(self, p):
        '''variable_declarators : variable_declarator
                                | variable_declarators ',' variable_declarator'''
        self.gen(p, 'variable_declarators')
        p[0].nodeType = deepcopy(p[1].nodeType)
        self.tac.curTempCnt = 0

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_variable_declarator(self, p):
        '''variable_declarator : variable_declarator_id
                               | variable_declarator_id '=' variable_initializer'''
        self.gen(p, 'variable_declarator', self.binary(p))

        # if first declaration then no comma else a comma exists
        typeSource = p[-2] if p[-1] is ',' else p[-1]
        lastTable = self.symTabStack[-1]
        varName = p[1].qualName[0]

        # Only one among the typeSource and variable_declarator_id should
        # have dimension information
        p[0].nodeType = self.resolveType(typeSource, p[1])

        p[0].qualName = varName

        # Check if already declared
        # If declared, then print an error and continue, else add to symbol table
        if lastTable.get(varName):
            print('Variable \'{}\' at line # {} already defined in the same scope at line # {}'.format(varName, self.lexer.lineno, lastTable[varName]['lineNo']))
        else:
            lastTable[varName] = {}
            lastTable[varName]['type'] = p[0].nodeType
            lastTable[varName]['lineNo'] = self.lexer.lineno

            # If a primitive data type, then get size from the GST
            # else allocate on heap and store pointer
            lastTable[varName]['size'] = 4
            if self.gst.get(p[0].nodeType.baseType):
                if self.gst[p[0].nodeType.baseType]['desc'] == 'primitive_type':
                    lastTable[varName]['size'] = self.gst[p[0].nodeType.baseType]['size']

            # set offset for new variable(s) and update the offset value in symbol table
            lastTable[varName]['offset'] = lastTable['size'] + lastTable[varName]['size']
            lastTable['size'] = lastTable[varName]['offset']

            if len(p) == 4:
                self.checkTypeAssignment(p[0], p[3])

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_variable_declarator_id(self, p):
        '''variable_declarator_id : NAME dims_opt'''
        self.gen(p, 'variable_declarator_id')
        p[0].qualName = [p[1].astName]
        if p[2]:
            p[0].nodeType.dim = p[2].nodeType.dim

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_variable_initializer(self, p):
        '''variable_initializer : expression
                                | array_initializer'''
        self.gen(p, 'variable_initializer')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_statement(self, p):
        '''statement : statement_without_trailing_substatement
                     | labeled_statement
                     | if_then_statement
                     | if_then_else_statement
                     | while_statement
                     | for_statement'''
        self.gen(p, 'statement')
        self.tac.curTempCnt = 0

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_statement_without_trailing_substatement(self, p):
        '''statement_without_trailing_substatement : block
                                                   | expression_statement
                                                   | assert_statement
                                                   | empty_statement
                                                   | switch_statement
                                                   | do_statement
                                                   | break_statement
                                                   | continue_statement
                                                   | return_statement'''
        self.gen(p, 'statement_without_trailing_substatement')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_expression_statement(self, p):
        '''expression_statement : statement_expression ';' '''
        self.gen(p, 'expression_statement')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_statement_expression(self, p):
        '''statement_expression : assignment
                                | pre_increment_expression
                                | pre_decrement_expression
                                | post_increment_expression
                                | post_decrement_expression
                                | method_invocation
                                | class_instance_creation_expression'''
        self.gen(p, 'statement_expression')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_comma_opt(self, p):
        '''comma_opt : ','
                     | empty'''
        self.gen(p, 'comma_opt')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_array_initializer(self, p):
        '''array_initializer : '{' comma_opt '}' '''
        self.gen(p, 'array_initializer')
        p[0].nodeType.baseType = 'void'
        p[0].nodeType.dim = [0]
        #  unknown data type and zero length of array

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_array_initializer2(self, p):
        '''array_initializer : '{' variable_initializers '}'
                             | '{' variable_initializers ',' '}' '''
        self.gen(p, 'array_initializer')
        p[0].nodeType = deepcopy(p[2].nodeType)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_variable_initializers(self, p):
        '''variable_initializers : variable_initializer
                                 | variable_initializers ',' variable_initializer'''
        self.gen(p, 'variable_initializers')
        if len(p) == 2:
            p[0].nodeType.dim = [1] + p[0].nodeType.dim
        else:
            if p[1].nodeType.dim[1:] == p[3].nodeType.dim:
                p[0].nodeType = deepcopy(p[1].nodeType)
                p[0].nodeType.dim[0] += 1
            else:
                print('Arrays elements not of same type at line #{}'.format(self.lexer.lineno))

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_method_invocation(self, p):
        '''method_invocation : NAME '(' argument_list_opt ')' '''
        self.gen(p, 'method_invocation')

        # fetch the symbol table entry for method
        func = self.findVar([p[1].astName])
        node_type = self.checkMethodInvocation(func, p[1].astName,
                p[3].nodeType if p[3] else [])

        if node_type:
            p[0].nodeType = deepcopy(node_type)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_method_invocation2(self, p):
        '''method_invocation : name '.' NAME '(' argument_list_opt ')'
                             | primary '.' NAME '(' argument_list_opt ')' '''
        self.gen(p, 'method_invocation')

        # fetch the symbol table entry for method
        if p[1].astName == 'name':
            func = self.findVar(p[1].qualName + [p[3].astName])
        else:
            func = self.findAttribute(p[1].nodeType, p[3].astName)

        # fetch the return type, false if no function exists
        node_type = self.checkMethodInvocation(func, p[3].astName,
                p[5].nodeType if p[5] else [])

        if node_type:
            p[0].nodeType = deepcopy(node_type)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_labeled_statement(self, p):
        '''labeled_statement : label ':' statement'''
        self.gen(p, 'labeled_statement')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_labeled_statement_no_short_if(self, p):
        '''labeled_statement_no_short_if : label ':' statement_no_short_if'''
        self.gen(p, 'labeled_statement_no_short_if')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_label(self, p):
        '''label : NAME'''
        self.gen(p, 'label')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_if_then_statement(self, p):
        '''if_then_statement : IF '(' expression ')' statement N'''
        self.gen(p, 'if_then_statement')

        self.tac.backpatch(p[3].tacLists.trueList, p[3].codeEnd)
        p[0].tacLists = deepcopy(p[5].tacLists)
        p[0].tacLists.nextList += p[3].tacLists.falseList + p[6].tacLists.nextList

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def tacIf(self, p):
        self.tac.backpatch(p[3].tacLists.trueList, p[3].codeEnd)
        self.tac.backpatch(p[3].tacLists.falseList, p[6].codeEnd)
        p[0].tacLists = p[5].tacLists + p[6].tacLists + p[8].tacLists

    def p_if_then_else_statement(self, p):
        '''if_then_else_statement : IF '(' expression ')' statement_no_short_if N ELSE statement'''
        self.gen(p, 'if_then_else_statement')
        self.tacIf(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_if_then_else_statement_no_short_if(self, p):
        '''if_then_else_statement_no_short_if : IF '(' expression ')' statement_no_short_if N ELSE statement_no_short_if'''
        self.gen(p, 'if_then_else_statement_no_short_if')
        self.tacIf(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def tacWhile(self, p):
        W, M, E, S, N = p[0], p[2], p[4], p[6], p[7]
        self.tac.backpatch(E.tacLists.trueList, E.codeEnd)
        self.tac.backpatch(S.tacLists.nextList + N.tacLists.nextList,
                M.codeEnd)
        self.tac.backpatch(S.tacLists.contList, M.codeEnd)
        S.tacLists.nextList = E.tacLists.falseList + S.tacLists.brkList

    def p_while_statement(self, p):
        '''while_statement : WHILE M '(' expression ')' statement N'''
        self.gen(p, 'while_statement')
        self.tacWhile(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_while_statement_no_short_if(self, p):
        '''while_statement_no_short_if : WHILE M '(' expression ')' statement_no_short_if N'''
        self.gen(p, 'while_statement_no_short_if')
        self.tacWhile(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_seen_FOR(self, p):
        '''seen_FOR : empty'''
        self.appendNewScope('for')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def tacFor(self, p):
        F, S1, C, S2, N2, S3, N3 = p[0], p[4], p[6], p[8], p[9], p[11], p[12]

        F.tacLists.nextList = C.tacLists.falseList + S3.tacLists.brkList
        self.tac.backpatch(S1.tacLists.nextList, S1.codeEnd)
        self.tac.backpatch(S2.tacLists.nextList + N2.tacLists.nextList, S1.codeEnd)
        self.tac.backpatch(S3.tacLists.nextList + N3.tacLists.nextList + S3.tacLists.contList,
                C.codeEnd)
        self.tac.backpatch(C.tacLists.trueList, N2.codeEnd)

    def p_for_statement(self, p):
        '''for_statement : FOR seen_FOR '(' for_init_opt ';' expression_opt ';' for_update_opt N ')' statement N'''
        self.gen(p, 'for_statement')
        self.endCurrScope()
        self.tacFor(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_for_statement_no_short_if(self, p):
        '''for_statement_no_short_if : FOR seen_FOR '(' for_init_opt ';' expression_opt ';' for_update_opt N ')' statement_no_short_if N'''
        self.gen(p, 'for_statement_no_short_if')
        self.endCurrScope()
        self.tacFor(p)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_for_init_opt(self, p):
        '''for_init_opt : for_init
                        | empty'''
        self.gen(p, 'for_init_opt')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_for_init(self, p):
        '''for_init : statement_expression_list
                    | local_variable_declaration'''
        self.gen(p, 'for_init')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_statement_expression_list(self, p):
        '''statement_expression_list : statement_expression
                                     | statement_expression_list ',' statement_expression'''
        self.gen(p, 'statement_expression_list')

        self.tac.curTempCnt = 0

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_expression_opt(self, p):
        '''expression_opt : expression
                          | empty'''
        self.gen(p, 'expression_opt')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_for_update_opt(self, p):
        '''for_update_opt : for_update
                          | empty'''
        self.gen(p, 'for_update_opt')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_for_update(self, p):
        '''for_update : statement_expression_list'''
        self.gen(p, 'for_update')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_statement_no_short_if(self, p):
        '''statement_no_short_if : statement_without_trailing_substatement
                                 | labeled_statement_no_short_if
                                 | if_then_else_statement_no_short_if
                                 | while_statement_no_short_if
                                 | for_statement_no_short_if'''
        self.gen(p, 'statement_no_short_if')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_assert_statement(self, p):
        '''assert_statement : ASSERT expression ';'
                            | ASSERT expression ':' expression ';' '''
        self.gen(p, 'assert_statement')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_empty_statement(self, p):
        '''empty_statement : ';' '''
        self.gen(p, 'empty_statement')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_switch_statement(self, p):
        '''switch_statement : SWITCH '(' expression ')' switch_block'''
        self.gen(p, 'switch_statement')

        # p[0].tacLists = deepcopy(p[5].tacLists)
        # p[0].tacLists.nextList = p[5].tacLists.nextList + p[5].tacLists.brkList
        # p[0].tacLists.brkList = []

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_switch_block(self, p):
        '''switch_block : '{' '}' '''
        self.gen(p, 'switch_block')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_switch_block2(self, p):
        '''switch_block : '{' switch_block_statements '}' '''
        self.gen(p, 'switch_block')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_switch_block3(self, p):
        '''switch_block : '{' switch_labels '}' '''
        self.gen(p, 'switch_block')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_switch_block4(self, p):
        '''switch_block : '{' switch_block_statements switch_labels '}' '''
        self.gen(p, 'switch_block')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_switch_block_statements(self, p):
        '''switch_block_statements : switch_block_statement
                                   | switch_block_statements switch_block_statement'''
        self.gen(p, 'switch_block_statements')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_switch_block_statement(self, p):
        '''switch_block_statement : switch_labels block_statements'''
        self.gen(p, 'switch_block_statement')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_switch_labels(self, p):
        '''switch_labels : switch_label
                         | switch_labels switch_label'''
        self.gen(p, 'switch_labels')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_switch_label(self, p):
        '''switch_label : CASE constant_expression ':'
                        | DEFAULT ':' '''
        self.gen(p, 'switch_label')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_constant_expression(self, p):
        '''constant_expression : expression'''
        self.gen(p, 'constant_expression')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_do_statement(self, p):
        '''do_statement : DO M statement WHILE '(' expression ')' ';' '''
        self.gen(p, 'do_statement')

        D, M, S, E = p[0], p[2], p[3], p[6]

        self.tac.backpatch(S.tacLists.nextList + S.tacLists.contList,
                S.codeEnd)
        self.tac.backpatch(E.tacLists.trueList, M.codeEnd)
        D.tacLists.nextList = E.tacLists.falseList + S.tacLists.brkList

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_break_statement(self, p):
        '''break_statement : BREAK ';'
                           | BREAK NAME ';' '''
        self.gen(p, 'break_statement')

        p[0].tacLists.brkList = [self.tac.nextquad()]
        self.tac.emit('JMP')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_continue_statement(self, p):
        '''continue_statement : CONTINUE ';'
                              | CONTINUE NAME ';' '''
        self.gen(p, 'continue_statement')

        p[0].tacLists.contList = [self.tac.nextquad()]
        self.tac.emit('JMP')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_return_statement(self, p):
        '''return_statement : RETURN expression_opt ';' '''
        self.gen(p, 'return_statement')

        if p[2]:
            self.tac.emit('MOVE', '$2', p[2].temporary)

        self.tac.emit('loadaddress', '$31', '4($30)')
        self.tac.emit('JR', '$31')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_class_instance_creation_expression(self, p):
        '''class_instance_creation_expression : NEW class_type '(' argument_list_opt ')' class_body_opt'''
        self.gen(p, 'class_instance_creation_expression')

        # find the constructor in the class's symbol table entry
        class_entry = self.findVar(p[2].qualName)
        construct = self.findAttribute(Node.Type(baseType=
            class_entry['scope_name']), p[2].qualName[0])

        node_type = self.checkMethodInvocation(construct, p[2].qualName,
                p[4].nodeType if p[4] else [])

        if node_type:
            p[0].nodeType = deepcopy(node_type)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_class_body_opt(self, p):
        '''class_body_opt : class_body
                          | empty'''
        self.gen(p, 'class_body_opt')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_field_access(self, p):
        '''field_access : primary '.' NAME'''
        self.gen(p, 'field_access')

        data_node = self.findAttribute(p[1].nodeType, p[3].astName)
        p[0].temporary = p[1].temporary

        # if offset, then add to address
        if data_node['offset']:
            self.tac.emit('+', p[0].temporary, p[1].temporary, data_node['offset'])

        if data_node:
            p[0].nodeType = data_node['type']

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_array_access(self, p):
        '''array_access : name '[' expression ']'
                        | primary_no_new_array '[' expression ']' '''
        self.gen(p, 'array_access')
        if p[1].astName == 'name':
            self.resolveScope(p[1])

        p[0].nodeType = deepcopy(p[1].nodeType)

        if not p[1].nodeType.dim:
            print('Trying to dereference a non-array type variable {} on line #{}'.
                    format(p[1].qualName[-1], self.lexer.lineno))
        else:
            unitSize = 1;
            unitSize *= self.gst.get(p[1].nodeType.baseType)['size']
            for i in range(1,len(p[1].nodeType.dim)):
                # ensure we have the data for unit size
                assert p[1].nodeType.dim[i]
                unitSize *= p[1].nodeType.dim[i]

            p[0].temporary = self.tac.allotNewTemp()
            self.tac.emit('addi', p[0].temporary,'$0', unitSize)
            self.tac.emit('mul', p[3].temporary, p[0].temporary)
            self.tac.emit('mflo', p[0].temporary)
            self.tac.emit('add', p[0].temporary, p[1].temporary,
                    p[0].temporary)

            p[0].nodeType.dim = p[0].nodeType.dim[1:]

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_array_creation_with_array_initializer(self, p):
        '''array_creation_with_array_initializer : NEW primitive_type dim_with_or_without_exprs array_initializer
                                                 | NEW class_or_interface_type dim_with_or_without_exprs array_initializer'''
        self.gen(p, 'array_creation_with_array_initializer')
        p[0].nodeType.baseType = p[2].nodeType.baseType
        p[0].nodeType.dim = deepcopy(p[3].nodeType.dim)

        if not self.checkTypeAssignment(p[0], p[4]):
            print('Type mismatch, Can\'t initialize the array at line #{}'.
                    format(self.lexer.lineno))

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_dim_with_or_without_exprs(self, p):
        '''dim_with_or_without_exprs : dim_with_or_without_expr
                                     | dim_with_or_without_exprs dim_with_or_without_expr'''
        self.gen(p, 'dim_with_or_without_exprs')
        if len(p) == 3:
            p[0].nodeType.dim = p[1].nodeType.dim + p[2].nodeType.dim

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_dim_with_or_without_expr(self, p):
        '''dim_with_or_without_expr : '[' expression ']'
                                    | '[' ']' '''
        self.gen(p, 'dim_with_or_without_expr')
        p[0].nodeType.dim = [0]
        if len(p) == 4:
            node_type = p[2].nodeType
            if not self.checkTypeAssignment(Node.Type(baseType='int'),
                    node_type, ifNode=False):
                print('Not a valid array length type {}{} at line #{}'.format(
                    node_type.baseType, node_type.dim, self.lexer.lineno))
            else:
                if p[2].astName.isdigit():
                    p[0].nodeType.dim[0] = int(p[2].astName)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_array_creation_without_array_initializer(self, p):
        '''array_creation_without_array_initializer : NEW primitive_type dim_with_or_without_exprs
                                                    | NEW class_or_interface_type dim_with_or_without_exprs'''
        self.gen(p, 'array_creation_without_array_initializer')
        p[0].nodeType.dim = deepcopy(p[3].nodeType.dim)
        p[0].nodeType.baseType = p[2].nodeType.baseType

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()


class NameParser(BaseParser):

    def p_name(self, p):
        '''name : simple_name
                | qualified_name'''
        self.gen(p, 'name')
        p[0].astName = 'name'

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_simple_name(self, p):
        '''simple_name : NAME'''
        self.gen(p, 'simple_name')
        p[0].qualName = [p[0].astName]

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_qualified_name(self, p):
        '''qualified_name : name '.' simple_name'''
        self.gen(p, 'qualified_name')
        p[0].qualName = p[1].qualName + p[3].qualName

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()


class LiteralParser(BaseParser):

    def find_type(self, num):
        float_start = r'^[0-9]*\.[0-9]+'
        if re.search(float_start + r'(d|D)?$', num):
            return 'double'
        if re.search(float_start + r'(f|F)$', num):
            return 'float'

        int_start = r'^((0x[0-9a-fA-F]+)|(0[0-7]+)|(0|([1-9][0-9]*)))'
        if re.search(int_start + r'(l|L)$', num):
            return 'long'
        if re.search(int_start + r'$', num):
            return 'integer'
        return 'error'

    def p_literal(self, p):
        '''literal : NUM'''
        self.gen(p, 'literal')
        litType = self.find_type(p[0].astName)
        if litType == 'error':
            print('Not a matching type at line #{}'.format(self.lexer.lineno))
        p[0].nodeType.baseType = litType

        p[0].temporary = self.tac.allotNewTemp()
        asciiVal = int(p[1].astName)
        if abs(asciiVal) < 32768:
            # OPT
            self.tac.emit('addi', p[0].temporary, '$0', asciiVal)
        else:
            varName = self.tac.addDataInt(asciiVal)
            self.tac.emit('loadword', p[0].temporary, varName)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_literal1(self, p):
        '''literal : CHAR_LITERAL'''
        self.gen(p, 'literal')
        p[0].nodeType.baseType = 'char'

        p[0].temporary = self.tac.allotNewTemp()
        asciiVal = ord(p[1].astName)
        self.tac.emit('addi', p[0].temporary, '$0', asciiVal)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_literal2(self, p):
        '''literal : STRING_LITERAL'''
        self.gen(p, 'literal')
        p[0].nodeType.baseType = 'String'

        p[0].temporary = self.tac.allotNewTemp()
        varName = self.tac.addDataString(p[1].astName)
        self.tac.emit('loadaddress', p[0].temporary, varName)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_literal3(self, p):
        '''literal : TRUE
                   | FALSE'''
        self.gen(p, 'literal')
        p[0].nodeType.baseType = 'boolean'

        p[0].temporary = self.tac.allotNewTemp()
        asciiVal = 1 if p[1].astName == 'true' else 0
        self.tac.emit('addi', p[0].temporary, '$0', asciiVal)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_literal4(self, p):
        '''literal : NULL'''
        self.gen(p, 'literal')
        p[0].nodeType.baseType = 'null'

        p[0].temporary = self.tac.allotNewTemp()
        self.tac.emit('add', p[0].temporary, '$0', '$0')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()


class TypeParser(BaseParser):

    def p_modifiers_opt(self, p):
        '''modifiers_opt : modifiers'''
        self.gen(p, 'modifiers_opt')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_modifiers_opt2(self, p):
        '''modifiers_opt : empty'''
        self.gen(p, 'modifiers_opt')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_modifiers(self, p):
        '''modifiers : modifier
                     | modifiers modifier'''
        self.gen(p, 'modifiers')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_modifier(self, p):
        '''modifier : PUBLIC
                    | PROTECTED
                    | PRIVATE
                    | STATIC
                    | ABSTRACT
                    | FINAL
                    | NATIVE
                    | TRANSIENT
                    | VOLATILE
                    | STRICTFP'''
        self.gen(p, 'modifier')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_type(self, p):
        '''type : primitive_type
                | reference_type'''
        self.gen(p, 'type')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

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
        self.gen(p, 'primitive_type')
        p[0].nodeType.baseType = p[0].astName

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_reference_type(self, p):
        '''reference_type : class_or_interface_type
                          | array_type'''
        self.gen(p, 'reference_type')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_class_or_interface_type(self, p):
        '''class_or_interface_type : class_or_interface'''
        self.gen(p, 'class_or_interface_type')
        # Not implementing generic_type

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_class_type(self, p):
        '''class_type : class_or_interface_type'''
        self.gen(p, 'class_type')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_class_or_interface(self, p):
        '''class_or_interface : name'''
        self.gen(p, 'class_or_interface')
        p[0].nodeType.baseType = p[0].qualName[0]
        #  p[0]['type'] = p[0]['name']

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_array_type(self, p):
        '''array_type : primitive_type dims
                      | name dims'''
        self.gen(p, 'array_type')
        if p[1].astName == 'name':
            p[1].astName = p[1].qualName[0]
        p[0].nodeType.baseType = p[1].astName
        p[0].nodeType.dim = p[2].nodeType.dim

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()


class ClassParser(BaseParser):

    def p_type_declaration(self, p):
        '''type_declaration : class_declaration'''
        self.gen(p, 'type_declaration')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_type_declaration2(self, p):
        '''type_declaration : ';' '''
        self.gen(p, 'type_declaration')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_class_declaration(self, p):
        '''class_declaration : class_header class_body'''
        self.gen(p, 'class_declaration')
        self.endCurrScope()

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_class_header(self, p):
        '''class_header : class_header_name'''
        self.gen(p, 'class_header')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_class_header_name(self, p):
        '''class_header_name : class_header_name1'''
        self.gen(p, 'class_header_name')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_class_header_name1(self, p):
        '''class_header_name1 : modifiers_opt CLASS NAME'''
        self.gen(p, 'class_header_name1')
        self.startNewScope(p[3].astName, 'class')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_class_body(self, p):
        '''class_body : '{' class_body_declarations_opt '}' '''
        self.gen(p, 'class_body')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_class_body_declarations_opt(self, p):
        '''class_body_declarations_opt : class_body_declarations'''
        self.gen(p, 'class_body_declarations_opt')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_class_body_declarations_opt2(self, p):
        '''class_body_declarations_opt : empty'''
        self.gen(p, 'class_body_declarations_opt')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_class_body_declarations(self, p):
        '''class_body_declarations : class_body_declaration
                                   | class_body_declarations class_body_declaration'''
        self.gen(p, 'class_body_declarations')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_class_body_declaration(self, p):
        '''class_body_declaration : class_member_declaration
                                  | static_initializer
                                  | constructor_declaration'''
        self.gen(p, 'class_body_declaration')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_class_body_declaration2(self, p):
        '''class_body_declaration : block'''
        self.gen(p, 'class_body_declaration')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_class_member_declaration(self, p):
        '''class_member_declaration : field_declaration
                                    | method_declaration'''
        self.gen(p, 'class_member_declaration')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_class_member_declaration2(self, p):
        '''class_member_declaration : ';' '''
        self.gen(p, 'class_member_declaration')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_field_declaration(self, p):
        '''field_declaration : modifiers_opt type variable_declarators ';' '''
        self.gen(p, 'field_declaration')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_static_initializer(self, p):
        '''static_initializer : STATIC block'''
        self.gen(p, 'static_initializer')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_constructor_declaration(self, p):
        '''constructor_declaration : constructor_header method_body'''
        self.gen(p, 'constructor_declaration')
        self.endCurrScope()

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_constructor_header(self, p):
        '''constructor_header : constructor_header_name formal_parameter_list_opt ')' '''
        self.gen(p, 'constructor_header')
        currScope = self.symTabStack[-1]
        currScope['size'] = 0

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_constructor_header_name(self, p):
        '''constructor_header_name : modifiers_opt NAME '(' '''
        self.gen(p, 'constructor_header_name')
        name = p[2].astName
        self.startNewScope(name, 'constructor')
        currScope = self.symTabStack[-1]
        currScope['type'] = Node.Type(baseType=name)
        currScope['size'] = -8

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_formal_parameter_list_opt(self, p):
        '''formal_parameter_list_opt : formal_parameter_list'''
        self.gen(p, 'formal_parameter_list_opt')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_formal_parameter_list_opt2(self, p):
        '''formal_parameter_list_opt : empty'''
        self.gen(p, 'formal_parameter_list_opt')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_formal_parameter_list(self, p):
        '''formal_parameter_list : formal_parameter
                                 | formal_parameter_list ',' formal_parameter'''
        self.gen(p, 'formal_parameter_list')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_formal_parameter(self, p):
        '''formal_parameter : modifiers_opt type variable_declarator_id
                            | modifiers_opt type ELLIPSIS variable_declarator_id'''

        self.gen(p, 'formal_parameter')
        # TODO Deal with Ellipsis

        currScope = self.symTabStack[-1]
        if not currScope.get('parList'):
            currScope['parList'] = []

        # using a prefix 'var_' for all variables in symbol table
        vdid = p[3] if len(p) == 4 else p[4]
        varName = vdid.qualName[0]

        if len(vdid.qualName) != 1:
            print("variable identifier expected instead of {} at line #{}".
                    format(vdid.qualName, self.lexer.lineno))

        # Err: check if type has been defined or not
        p[0].nodeType = self.resolveType(p[2], vdid)
        p[0].qualName = varName

        # Check if already declared
        # If declared, then print an error and continue, else add to symbol table
        if currScope.get(varName):
            print('Function Parameter \'{}\' at line #{} already defined in the same parameter list'.format(varName, self.lexer.lineno))
        else:
            currScope[varName] = {}
            currScope[varName]['type'] = p[0].nodeType
            currScope[varName]['lineNo'] = self.lexer.lineno

            currScope[varName]['size'] = 4
            if self.gst.get(p[0].nodeType.baseType):
                if self.gst[p[0].nodeType.baseType]['desc'] == 'primitive_type':
                    currScope[varName]['size'] = max(4, self.gst[p[0].nodeType.baseType]['size'])

            # set offset for new variable(s) and update the offset value in symbol table
            # Negative offset, as according to function stack
            currScope[varName]['offset'] = currScope['size']
            currScope['size'] = currScope[varName]['offset'] - currScope[varName]['size']

            # append in Parameter List
            currScope['parList'].append(varName)

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_method_body(self, p):
        '''method_body : '{' block_statements_opt '}' '''
        self.gen(p, 'method_body')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_method_declaration(self, p):
        '''method_declaration : abstract_method_declaration
                              | method_header method_body'''
        self.gen(p, 'method_declaration')
        self.endCurrScope()

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_abstract_method_declaration(self, p):
        '''abstract_method_declaration : method_header ';' '''
        self.gen(p, 'abstract_method_declaration')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_method_header(self, p):
        '''method_header : method_header_name formal_parameter_list_opt ')' method_header_extended_dims'''
        self.gen(p, 'method_header')
        currScope = self.symTabStack[-1]
        currScope['size'] = 0

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_method_header_name(self, p):
        '''method_header_name : modifiers_opt type NAME '(' '''
        name = p[3]
        self.startNewScope(name, 'method')
        currScope = self.symTabStack[-1]
        currScope['size'] = -8
        currScope['type'] = p[2].nodeType
        currScope['tacStart'] = self.tac.nextquad()
        self.gen(p, 'method_header_name')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_method_header_extended_dims(self, p):
        '''method_header_extended_dims : dims_opt'''
        self.gen(p, 'method_header_extended_dims')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_argument_list_opt(self, p):
        '''argument_list_opt : argument_list'''
        self.gen(p, 'argument_list_opt')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_argument_list_opt2(self, p):
        '''argument_list_opt : empty'''
        self.gen(p, 'argument_list_opt')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_argument_list(self, p):
        '''argument_list : expression
                         | argument_list ',' expression'''
        self.gen(p, 'argument_list')
        if len(p) == 2:
            p[0].nodeType = [p[0].nodeType]
        else:
            p[0].nodeType = p[1].nodeType + [p[3].nodeType]

        self.tac.curTempCnt = 0

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()


class CompilationUnitParser(BaseParser):

    def p_compilation_unit(self, p):
        '''compilation_unit : package_declaration'''
        self.gen(p, 'compilation_unit')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_compilation_unit2(self, p):
        '''compilation_unit : package_declaration import_declarations'''
        self.gen(p, 'compilation_unit')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_compilation_unit3(self, p):
        '''compilation_unit : package_declaration import_declarations type_declarations'''
        self.gen(p, 'compilation_unit')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_compilation_unit4(self, p):
        '''compilation_unit : package_declaration type_declarations'''
        self.gen(p, 'compilation_unit')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_compilation_unit5(self, p):
        '''compilation_unit : import_declarations'''
        self.gen(p, 'compilation_unit')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_compilation_unit6(self, p):
        '''compilation_unit : type_declarations'''
        self.gen(p, 'compilation_unit')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_compilation_unit7(self, p):
        '''compilation_unit : import_declarations type_declarations'''
        self.gen(p, 'compilation_unit')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_compilation_unit8(self, p):
        '''compilation_unit : empty'''
        self.gen(p, 'compilation_unit')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_package_declaration(self, p):
        '''package_declaration : package_declaration_name ';' '''
        self.gen(p, 'package_declaration')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_package_declaration_name(self, p):
        '''package_declaration_name : modifiers PACKAGE name
                                    | PACKAGE name'''
        self.gen(p, 'package_declaration_name')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_import_declarations(self, p):
        '''import_declarations : import_declaration
                               | import_declarations import_declaration'''
        self.gen(p, 'import_declarations')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_import_declaration(self, p):
        '''import_declaration : single_type_import_declaration
                              | type_import_on_demand_declaration
                              | single_static_import_declaration
                              | static_import_on_demand_declaration'''
        self.gen(p, 'import_declaration')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_single_type_import_declaration(self, p):
        '''single_type_import_declaration : IMPORT name ';' '''
        self.gen(p, 'single_type_import_declaration')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_type_import_on_demand_declaration(self, p):
        '''type_import_on_demand_declaration : IMPORT name '.' '*' ';' '''
        self.gen(p, 'type_import_on_demand_declaration')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_single_static_import_declaration(self, p):
        '''single_static_import_declaration : IMPORT STATIC name ';' '''
        self.gen(p, 'single_static_import_declaration')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_static_import_on_demand_declaration(self, p):
        '''static_import_on_demand_declaration : IMPORT STATIC name '.' '*' ';' '''
        self.gen(p, 'static_import_on_demand_declaration')

        if p[0]:
            p[0].codeEnd = self.tac.nextquad()

    def p_type_declarations(self, p):
        '''type_declarations : type_declaration
                             | type_declarations type_declaration'''
        self.gen(p, 'type_declarations')
