from BaseParser import BaseParser
import re

class ExpressionParser(BaseParser):

    def p_expression(self, p):
        '''expression : assignment_expression'''
        self.gen(p, 'expression')

    def p_expression_not_name(self, p):
        '''expression_not_name : assignment_expression_not_name'''
        self.gen(p, 'expression_not_name')

    def p_assignment_expression(self, p):
        '''assignment_expression : assignment
                                 | conditional_expression'''
        self.gen(p, 'assignment_expression')

    def p_assignment_expression_not_name(self, p):
        '''assignment_expression_not_name : assignment
                                          | conditional_expression_not_name'''
        self.gen(p, 'assignment_expression_not_name')

    def p_assignment(self, p):
        '''assignment : postfix_expression assignment_operator assignment_expression'''
        self.gen(p, 'assignment', self.binary(p))
        p[0]['type'], p[0]['reference'] = p[1]['type'], p[1]['reference']
        #  if p[0]['astName'] == '=':

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

    def binary_exp_cond(self, p):
        if len(p) == 2:
            return

        if p[1]['astName'] == 'name':
            p[1]['astName'] = p[1]['name']
            symTabEntry = findVar(p[1])
            p[1]['type'], p[1]['reference'] = symTabEntry['type'], symTabEntry['reference']

        p[0]['type'], p[0]['reference'] = 'boolean', []

        if p[1]['type'] != 'boolean':
            print('Incompatible type on line #{}: {} {} can\'t be converted \
                    to boolean'.format(self.lexer.lineno, p[1]['type'], p[1]['reference']))

        if p[3]['type'] == p[5]['type'] and p[3]['reference'] == p[5]['reference']:
            p[0]['type'], p[0]['reference'] = p[3]['type'], p[3]['reference']
        else:
            newType = self.convertible(p[3], p[5])
            if newType:
                p[0]['type'] = newType
                p[0]['reference'] = []
            else:
                print('Not matching types for conditional expression at line #{}'.format(
                    self.lexer.lineno))

    def p_conditional_expression(self, p):
        '''conditional_expression : conditional_or_expression
                                  | conditional_or_expression '?' expression ':' conditional_expression'''
        self.gen(p, 'conditional_expression')
        self.binary_exp_cond(p)

    def p_conditional_expression_not_name(self, p):
        '''conditional_expression_not_name : conditional_or_expression_not_name
                                           | conditional_or_expression_not_name '?' expression ':' conditional_expression
                                           | name '?' expression ':' conditional_expression'''
        self.gen(p, 'conditional_expression_not_name')
        self.binary_exp_cond(p)

    def binary_exp_bool(self, p):
        if len(p) == 2:
            return

        if p[1]['astName'] == 'name':
            p[1]['astName'] = p[1]['name']
            symTabEntry = findVar(p[1])
            p[1]['type'], p[1]['reference'] = symTabEntry['type'], symTabEntry['reference']

        p[0]['type'], p[0]['reference'] = 'boolean', []

        type1, type2 = p[1]['type'], p[3]['type']
        if type1 != 'boolean' and type2 != 'boolean':
            print('Conditional allowed only on boolean: {} at line #{}'.format(
                p[0]['astname'], self.lexer.lineno))

    def p_conditional_or_expression(self, p):
        '''conditional_or_expression : conditional_and_expression
                                     | conditional_or_expression OR conditional_and_expression'''
        self.gen(p, 'conditional_or_expression', self.binary(p))
        self.binary_exp_bool(p)

    def p_conditional_or_expression_not_name(self, p):
        '''conditional_or_expression_not_name : conditional_and_expression_not_name
                                              | conditional_or_expression_not_name OR conditional_and_expression
                                              | name OR conditional_and_expression'''
        self.gen(p, 'conditional_or_expression_not_name', self.binary(p))
        self.binary_exp_bool(p)

    def p_conditional_and_expression(self, p):
        '''conditional_and_expression : inclusive_or_expression
                                      | conditional_and_expression AND inclusive_or_expression'''
        self.gen(p, 'conditional_and_expression', self.binary(p))
        self.binary_exp_bool(p)

    def p_conditional_and_expression_not_name(self, p):
        '''conditional_and_expression_not_name : inclusive_or_expression_not_name
                                               | conditional_and_expression_not_name AND inclusive_or_expression
                                               | name AND inclusive_or_expression'''
        self.gen(p, 'conditional_and_expression_not_name', self.binary(p))
        self.binary_exp_bool(p)

    def binary_exp_bitwise(self, p):
        if len(p) == 2:
            return

        if p[1]['astName'] == 'name':
            p[1]['astName'] = p[1]['name']
            symTabEntry = findVar(p[1])
            p[1]['type'], p[1]['reference'] = symTabEntry['type'], symTabEntry['reference']

        type1, type2 = p[1]['type'], p[3]['type']
        if type1 == 'boolean' and type2 == 'boolean':
            p[0]['type'], p[0]['reference'] = 'boolean', []
        elif type1 in self.intsChar and type2 in self.intsChar:
            if type1 == 'long' or type2 == 'long':
                p[0]['type'], p[0]['reference'] = 'long', []
            else:
                p[0]['type'], p[0]['reference'] = 'int', []
        else:
            p[0]['type'], p[0]['reference'] = 'int', []
            print('Incompatible types around the operator {} at line #{}'.format(
                p[2]['astName'], self.lexer.lineno))

    def p_inclusive_or_expression(self, p):
        '''inclusive_or_expression : exclusive_or_expression
                                   | inclusive_or_expression '|' exclusive_or_expression'''
        self.gen(p, 'inclusive_or_expression', self.binary(p))
        self.binary_exp_bitwise(p)

    def p_inclusive_or_expression_not_name(self, p):
        '''inclusive_or_expression_not_name : exclusive_or_expression_not_name
                                            | inclusive_or_expression_not_name '|' exclusive_or_expression
                                            | name '|' exclusive_or_expression'''
        self.gen(p, 'inclusive_or_expression_not_name', self.binary(p))
        self.binary_exp_bitwise(p)

    def p_exclusive_or_expression(self, p):
        '''exclusive_or_expression : and_expression
                                   | exclusive_or_expression '^' and_expression'''
        self.gen(p, 'exclusive_or_expression', self.binary(p))
        self.binary_exp_bitwise(p)

    def p_exclusive_or_expression_not_name(self, p):
        '''exclusive_or_expression_not_name : and_expression_not_name
                                            | exclusive_or_expression_not_name '^' and_expression
                                            | name '^' and_expression'''
        self.gen(p, 'exclusive_or_expression_not_name', self.binary(p))
        self.binary_exp_bitwise(p)

    def p_and_expression(self, p):
        '''and_expression : equality_expression
                          | and_expression '&' equality_expression'''
        self.gen(p, 'and_expression', self.binary(p))
        self.binary_exp_bitwise(p)

    def p_and_expression_not_name(self, p):
        '''and_expression_not_name : equality_expression_not_name
                                   | and_expression_not_name '&' equality_expression
                                   | name '&' equality_expression'''
        self.gen(p, 'and_expression_not_name', self.binary(p))
        self.binary_exp_bitwise(p)

    def binary_exp_rel(self, p):
        if len(p) == 2:
            return

        if p[1]['astName'] == 'name':
            p[1]['astName'] = p[1]['name']
            symTabEntry = findVar(p[1])
            p[1]['type'], p[1]['reference'] = symTabEntry['type'], symTabEntry['reference']

        p[0]['type'], p[0]['reference'] = 'boolean', []

        type1, type2 = p[1]['type'], p[3]['type']
        oper = p[2]['astName']
        if oper == 'instanceof':
            pass
        elif type1 == type2:
            if type1 in self.numsChar:
                pass
            elif (oper == '==' or oper == '!=') and type1 == 'boolean':
                pass
            else:
                print('Incompatible operator {} with boolean type line #{}'.format(
                    oper, self.lexer.lineno))
        else:
            print('Not matching types for {} at line #{}'.format(p[0]['astName'], self.lexer.lineno))

    def p_equality_expression(self, p):
        '''equality_expression : instanceof_expression
                               | equality_expression EQ instanceof_expression
                               | equality_expression NEQ instanceof_expression'''
        self.gen(p, 'equality_expression', self.binary(p))
        self.binary_exp_rel(p)

    def p_equality_expression_not_name(self, p):
        '''equality_expression_not_name : instanceof_expression_not_name
                                        | equality_expression_not_name EQ instanceof_expression
                                        | name EQ instanceof_expression
                                        | equality_expression_not_name NEQ instanceof_expression
                                        | name NEQ instanceof_expression'''
        self.gen(p, 'equality_expression_not_name', self.binary(p))
        self.binary_exp_rel(p)

    def p_instanceof_expression(self, p):
        '''instanceof_expression : relational_expression
                                 | instanceof_expression INSTANCEOF reference_type'''
        self.gen(p, 'instanceof_expression', self.binary(p))

    def p_instanceof_expression_not_name(self, p):
        '''instanceof_expression_not_name : relational_expression_not_name
                                          | name INSTANCEOF reference_type
                                          | instanceof_expression_not_name INSTANCEOF reference_type'''
        self.gen(p, 'instanceof_expression_not_name', self.binary(p))

    def p_relational_expression(self, p):
        '''relational_expression : shift_expression
                                 | relational_expression '>' shift_expression
                                 | relational_expression '<' shift_expression
                                 | relational_expression GTEQ shift_expression
                                 | relational_expression LTEQ shift_expression'''
        self.gen(p, 'relational_expression', self.binary(p))
        self.binary_exp_rel(p)

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
        self.binary_exp_rel(p)

    def binary_exp_shift(self, p):
        if len(p) == 2:
            return

        if p[1]['astName'] == 'name':
            p[1]['astName'] = p[1]['name']
            symTabEntry = findVar(p[1])
            p[1]['type'], p[1]['reference'] = symTabEntry['type'], symTabEntry['reference']

        type1, type2 = p[1]['type'], p[3]['type']
        if type1 in self.intsChar and type2 in self.intsChar:
            p[0]['type'] = 'long' if (type1 == 'long' or type2 == 'long') else 'int'
            p[0]['reference'] = []
        else:
            p[0]['type'], p[0]['reference'] = 'int', []
            print('Not matching types for {} at line #{}'.format(p[0]['astName'], self.lexer.lineno))

    def p_shift_expression(self, p):
        '''shift_expression : additive_expression
                            | shift_expression LSHIFT additive_expression
                            | shift_expression RSHIFT additive_expression
                            | shift_expression RRSHIFT additive_expression'''
        self.gen(p, 'shift_expression', self.binary(p))
        self.binary_exp_shift(p)

    def p_shift_expression_not_name(self, p):
        '''shift_expression_not_name : additive_expression_not_name
                                     | shift_expression_not_name LSHIFT additive_expression
                                     | name LSHIFT additive_expression
                                     | shift_expression_not_name RSHIFT additive_expression
                                     | name RSHIFT additive_expression
                                     | shift_expression_not_name RRSHIFT additive_expression
                                     | name RRSHIFT additive_expression'''
        self.gen(p, 'shift_expression_not_name', self.binary(p))
        self.binary_exp_shift(p)

    def binary_exp_addmult(self, p):
        if len(p) == 2:
            return

        if p[1]['astName'] == 'name':
            p[1]['astName'] = p[1]['name']
            symTabEntry = findVar(p[1])
            p[1]['type'], p[1]['reference'] = symTabEntry['type'], symTabEntry['reference']

        type1, type2 = p[1]['type'], p[3]['type']
        if p[0]['astName'] != '%':
            if type1 in self.numsChar and type2 in self.numsChar:
                for type in ['double', 'float', 'long']:
                    if type1 == type or type2 == type:
                        p[0]['type'], p[0]['reference'] = type, []
                        break
                else:
                    p[0]['type'], p[0]['reference'] == 'int', []
            elif p[2]['astName'] == '+' and (type1 == "String" or type2 == "String"):
                p[0]['type'], p[0]['reference'] = 'String', []
            else:
                p[0]['type'], p[0]['reference'] = 'int', []
                print('Not matching types for {} at line #{}'.format(
                    p[0]['astName'], self.lexer.lineno))
        else:
            self.binary_exp_shift(p)

    def p_additive_expression(self, p):
        '''additive_expression : multiplicative_expression
                               | additive_expression '+' multiplicative_expression
                               | additive_expression '-' multiplicative_expression'''
        self.gen(p, 'additive_expression', self.binary(p))
        self.binary_exp_addmult(p)

    def p_additive_expression_not_name(self, p):
        '''additive_expression_not_name : multiplicative_expression_not_name
                                        | additive_expression_not_name '+' multiplicative_expression
                                        | name '+' multiplicative_expression
                                        | additive_expression_not_name '-' multiplicative_expression
                                        | name '-' multiplicative_expression'''
        self.gen(p, 'additive_expression_not_name', self.binary(p))
        self.binary_exp_addmult(p)

    def p_multiplicative_expression(self, p):
        '''multiplicative_expression : unary_expression
                                     | multiplicative_expression '*' unary_expression
                                     | multiplicative_expression '/' unary_expression
                                     | multiplicative_expression '%' unary_expression'''
        self.gen(p, 'multiplicative_expression', self.binary(p))
        self.binary_exp_addmult(p)

    def p_multiplicative_expression_not_name(self, p):
        '''multiplicative_expression_not_name : unary_expression_not_name
                                              | multiplicative_expression_not_name '*' unary_expression
                                              | name '*' unary_expression
                                              | multiplicative_expression_not_name '/' unary_expression
                                              | name '/' unary_expression
                                              | multiplicative_expression_not_name '%' unary_expression
                                              | name '%' unary_expression'''
        self.gen(p, 'multiplicative_expression_not_name', self.binary(p))
        self.binary_exp_addmult(p)


    def unary_exp_plus(self, p):
        if p[0]['astName'] in ['+', '-']:
            if p[1]['type'] in self.intsCharWoLong:
                p[0]['type'] = 'int'
            elif p[1]['type'] in self.decimals + ['long']:
                p[0]['type'] = p[2]['type']
            else:
                p[0]['type'] = 'int'
                print('Not a matching type for {} at line #{}'.format(
                    p[0]['astName'], self.lexer.lineno))
            p[0]['reference'] = []

    def p_unary_expression(self, p):
        '''unary_expression : pre_increment_expression
                            | pre_decrement_expression
                            | '+' unary_expression
                            | '-' unary_expression
                            | unary_expression_not_plus_minus'''
        self.gen(p, 'unary_expression', self.unary(p))
        self.unary_exp_plus(p)

    def p_unary_expression_not_name(self, p):
        '''unary_expression_not_name : pre_increment_expression
                                     | pre_decrement_expression
                                     | '+' unary_expression
                                     | '-' unary_expression
                                     | unary_expression_not_plus_minus_not_name'''
        self.gen(p, 'unary_expression_not_name', self.unary(p))
        self.unary_exp_plus(p)

    def p_pre_increment_expression(self, p):
        '''pre_increment_expression : PLUSPLUS unary_expression'''
        self.gen(p, 'pre_increment_expression', self.unary(p))
        self.unary_exp_post(self, p, 2)

    def p_pre_decrement_expression(self, p):
        '''pre_decrement_expression : MINUSMINUS unary_expression'''
        self.gen(p, 'pre_decrement_expression', self.unary(p))
        self.unary_exp_post(self, p, 2)

    def unary_exp_nots(self, p):
        if p[0]['astName'] == '~':
            p[0]['type'], p[0]['reference'] = 'int', []
            if p[2]['type'] in self.intsCharWoLong:
                pass
            elif p[2]['type'] == 'long':
                p[0]['type'] = p[2]['type']
            else:
                print('Not a matching type for ~ at line #{}'.format(
                    self.lexer.lineno))

        if p[0]['astName'] == '!':
            p[0]['type'], p[0]['reference'] = 'boolean'
            if p[2]['type'] != 'boolean':
                print('Not a matching type for ! at line #{}'.format(
                    self.lexer.lineno))

    def p_unary_expression_not_plus_minus(self, p):
        '''unary_expression_not_plus_minus : postfix_expression
                                           | '~' unary_expression
                                           | '!' unary_expression
                                           | cast_expression'''
        self.gen(p, 'unary_expression_not_plus_minus', self.unary(p))
        self.unary_exp_nots(p)

    def p_unary_expression_not_plus_minus_not_name(self, p):
        '''unary_expression_not_plus_minus_not_name : postfix_expression_not_name
                                                    | '~' unary_expression
                                                    | '!' unary_expression
                                                    | cast_expression'''
        self.gen(p, 'unary_expression_not_plus_minus_not_name', self.unary(p))
        self.unary_exp_nots(p)

    def p_postfix_expression(self, p):
        '''postfix_expression : primary
                              | name
                              | post_increment_expression
                              | post_decrement_expression'''
        self.gen(p, 'postfix_expression')
        if p[1]['astName'] == 'name':
            p[1]['astName'] = p[1]['name']
            symTabEntry = findVar(p[1])
            p[1]['type'] = symTabEntry['type']
            p[1]['reference'] = symTabEntry['reference']

    def p_postfix_expression_not_name(self, p):
        '''postfix_expression_not_name : primary
                                       | post_increment_expression
                                       | post_decrement_expression'''
        self.gen(p, 'postfix_expression_not_name')

    def unary_exp_post(self, p, index):
        p[0]['type'], p[0]['reference']= p[index]['type'], []
        if p[index]['type'] not in self.numsChar:
            print('Type error in post expression at line # {}'.format(self.lexer.lineno))

    def p_post_increment_expression(self, p):
        '''post_increment_expression : postfix_expression PLUSPLUS'''
        self.gen(p, 'post_increment_expression', 2)
        self.unary_exp_post(p, 1)

    def p_post_decrement_expression(self, p):
        '''post_decrement_expression : postfix_expression MINUSMINUS'''
        self.gen(p, 'post_decrement_expression', 2)
        self.unary_exp_post(p, 1)

    def p_primary(self, p):
        '''primary : primary_no_new_array
                   | array_creation_with_array_initializer
                   | array_creation_without_array_initializer'''
        self.gen(p, 'primary')

    def p_primary_no_new_array(self, p):
        '''primary_no_new_array : literal
                                | THIS
                                | class_instance_creation_expression
                                | field_access
                                | method_invocation
                                | array_access'''
        self.gen(p, 'primary_no_new_array')
        if p[0]['astName'] == 'this':
            pass
            # TODO

    def p_primary_no_new_array2(self, p):
        '''primary_no_new_array : '(' name ')'
                                | '(' expression_not_name ')' '''
        self.gen(p, 'primary_no_new_array')
        if p[2]['astName'] == 'name':
            p[1]['astName'] = p[1]['name']
            symTabEntry = self.findVar(p[2])
            p[2]['type'], p[2]['reference'] = symTabEntry['type'], symTabEntry['reference']
        p[0]['type'], p[0]['reference'] = p[2]['type'], p[2]['reference']

    def p_dims_opt(self, p):
        '''dims_opt : dims'''
        self.gen(p, 'dims_opt')

    def p_dims_opt2(self, p):
        '''dims_opt : empty'''
        self.gen(p, 'dims_opt')

    def p_dims(self, p):
        '''dims : dims_loop'''
        self.gen(p, 'dims')

    def p_dims_loop(self, p):
        '''dims_loop : one_dim_loop
                     | dims_loop one_dim_loop'''
        self.gen(p, 'dims_loop')
        p[0]['dim'] = p[1]['dim']
        if len(p) == 3:
            p[0]['dim'] += p[2]['dim']

    def p_one_dim_loop(self, p):
        '''one_dim_loop : '[' ']' '''
        self.gen(p, 'one_dim_loop')
        p[0]['dim'] = [0]

    def p_cast_expression(self, p):
        '''cast_expression : '(' primitive_type dims_opt ')' unary_expression'''
        self.gen(p, 'cast_expression')

    def p_cast_expression2(self, p):
        '''cast_expression : '(' name ')' unary_expression_not_plus_minus'''
        self.gen(p, 'cast_expression')

    def p_cast_expression3(self, p):
        '''cast_expression : '(' name dims ')' unary_expression_not_plus_minus'''
        self.gen(p, 'cast_expression')

class StatementParser(BaseParser):

    def p_block(self, p):
        ''' block : '{' seen_Lbrace block_statements_opt '}' '''
        self.gen(p, 'block')
        self.endCurrScope()

    def p_seen_Lbrace(self, p):
        '''seen_Lbrace : empty'''
        self.appendNewScope('block')

    def p_block_statements_opt(self, p):
        '''block_statements_opt : block_statements'''
        self.gen(p, 'block_statements_opt')

    def p_block_statements_opt2(self, p):
        '''block_statements_opt : empty'''
        self.gen(p, 'block_statements_opt')

    def p_block_statements(self, p):
        '''block_statements : block_statement
                            | block_statements block_statement'''
        self.gen(p, 'block_statements')

    def p_block_statement(self, p):
        '''block_statement : local_variable_declaration_statement
                           | statement
                           | class_declaration'''
        self.gen(p, 'block_statement')

    def p_local_variable_declaration_statement(self, p):
        '''local_variable_declaration_statement : local_variable_declaration ';' '''
        self.gen(p, 'local_variable_declaration_statement')

    def p_local_variable_declaration(self, p):
        '''local_variable_declaration : type variable_declarators'''
        self.gen(p, 'local_variable_declaration')

    def p_local_variable_declaration2(self, p):
        '''local_variable_declaration : modifiers type variable_declarators'''
        self.gen(p, 'local_variable_declaration')

    def p_variable_declarators(self, p):
        '''variable_declarators : variable_declarator
                                | variable_declarators ',' variable_declarator'''
        self.gen(p, 'variable_declarators')
        p[0]['type'] = p[1]['type']

    def p_variable_declarator(self, p):
        '''variable_declarator : variable_declarator_id
                               | variable_declarator_id '=' variable_initializer'''
        self.gen(p, 'variable_declarator', self.binary(p))

        # if first declaration then no comma else a comma exists
        typeSource = p[-2] if p[-1] is ',' else p[-1]
        p[0]['type'] = typeSource['type']

        # Only one among the typeSource and variable_declarator_id should
        # have dimension information
        p[0]['type'], p[0]['reference'] = self.resolveType(typeSource, p[1])

        # using a prefix 'var_' for all variables in symbol table
        lastTable = self.symTabStack[-1]
        varName = 'var_' + p[1]['varName']

        # Check if already declared
        # If declared, then print an error and continue, else add to symbol table
        if lastTable.get(varName):
            print('Variable \'{}\' at line # {} already defined in the same scope at line # {}'.format(p[1]['varName'], self.lexer.lineno, lastTable[varName]['lineNo']))
        else:
            lastTable[varName] = {}
            lastTable[varName]['type'] = p[0]['type']
            lastTable[varName]['lineNo'] = self.lexer.lineno

            # If a primitive data type, then get size from the GST
            # else allocate on heap and store pointer
            lastTable[varName]['size'] = 4
            if self.gst.get(p[0]['type']):
                if self.gst[p[0]['type']]['desc'] == 'primitive_type':
                    lastTable[varName]['size'] = self.gst[p[0]['type']]['size']

            # set offset for new variable(s) and update the offset value in symbol table
            lastTable[varName]['offset'] = lastTable['size'] + lastTable[varName]['size']
            lastTable['size'] = lastTable[varName]['offset']

            if len(p) == 4:
                if self.checkTypeAssignment(p[0], p[3], varName):
                    # reverse the dimensions
                    reference, dim = self.splitType(p[0]['reference'])
                    p[0]['reference'] = reference + dim[::-1] if isinstance(reference, list) else [reference] + dim[::-1]

            lastTable[varName]['reference'] = p[0]['reference']

    def p_variable_declarator_id(self, p):
        '''variable_declarator_id : NAME dims_opt'''
        self.gen(p, 'variable_declarator_id')
        p[0]['varName'] = p[1]['astName']
        if p[2]:
            p[0]['dim'] = p[2]['dim']

    def p_variable_initializer(self, p):
        '''variable_initializer : expression
                                | array_initializer'''
        self.gen(p, 'variable_initializer')
        if not p[1].get('type'):
            # TODO
            p[1]['type'] = 0

    def p_statement(self, p):
        '''statement : statement_without_trailing_substatement
                     | labeled_statement
                     | if_then_statement
                     | if_then_else_statement
                     | while_statement
                     | for_statement'''
        self.gen(p, 'statement')

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

    def p_expression_statement(self, p):
        '''expression_statement : statement_expression ';' '''
        self.gen(p, 'expression_statement')

    def p_statement_expression(self, p):
        '''statement_expression : assignment
                                | pre_increment_expression
                                | pre_decrement_expression
                                | post_increment_expression
                                | post_decrement_expression
                                | method_invocation
                                | class_instance_creation_expression'''
        self.gen(p, 'statement_expression')

    def p_comma_opt(self, p):
        '''comma_opt : ','
                     | empty'''
        self.gen(p, 'comma_opt')

    def p_array_initializer(self, p):
        '''array_initializer : '{' comma_opt '}' '''
        self.gen(p, 'array_initializer')
        # unknown data type and zero length of array
        p[0]['type'] = 'reference'
        p[0]['reference'] = [0, 0]

    def p_array_initializer2(self, p):
        '''array_initializer : '{' variable_initializers '}'
                             | '{' variable_initializers ',' '}' '''
        self.gen(p, 'array_initializer')
        p[0]['type'] = p[2]['type']
        p[0]['reference'] = p[2]['reference']

    def p_variable_initializers(self, p):
        '''variable_initializers : variable_initializer
                                 | variable_initializers ',' variable_initializer'''
        self.gen(p, 'variable_initializers')
        if len(p) == 2:
            if not p[0].get('reference'):
                p[0]['reference'] = [p[0]['type']]
                p[0]['type'] = 'reference'
            p[0]['reference'].append(1)
        else:
            # the following condition also ensures that the data type is same
            if p[1]['reference'][0:-1] == p[3]['reference']:
                p[0]['reference'] = p[1]['reference']
                p[0]['reference'][-1] += 1
            else:
                print('Arrays elements not of same type at line #{}'.format(self.lexer.lineno))

    def p_method_invocation(self, p):
        '''method_invocation : NAME '(' argument_list_opt ')' '''
        self.gen(p, 'method_invocation')

    def p_method_invocation2(self, p):
        '''method_invocation : name '.' NAME '(' argument_list_opt ')'
                             | primary '.' NAME '(' argument_list_opt ')' '''
        self.gen(p, 'method_invocation')

    def p_labeled_statement(self, p):
        '''labeled_statement : label ':' statement'''
        self.gen(p, 'labeled_statement')

    def p_labeled_statement_no_short_if(self, p):
        '''labeled_statement_no_short_if : label ':' statement_no_short_if'''
        self.gen(p, 'labeled_statement_no_short_if')

    def p_label(self, p):
        '''label : NAME'''
        self.gen(p, 'label')

    def p_if_then_statement(self, p):
        '''if_then_statement : IF '(' expression ')' statement'''
        self.gen(p, 'if_then_statement')

    def p_if_then_else_statement(self, p):
        '''if_then_else_statement : IF '(' expression ')' statement_no_short_if ELSE statement'''
        self.gen(p, 'if_then_else_statement')

    def p_if_then_else_statement_no_short_if(self, p):
        '''if_then_else_statement_no_short_if : IF '(' expression ')' statement_no_short_if ELSE statement_no_short_if'''
        self.gen(p, 'if_then_else_statement_no_short_if')

    def p_while_statement(self, p):
        '''while_statement : WHILE '(' expression ')' statement'''
        self.gen(p, 'while_statement')

    def p_while_statement_no_short_if(self, p):
        '''while_statement_no_short_if : WHILE '(' expression ')' statement_no_short_if'''
        self.gen(p, 'while_statement_no_short_if')

    def p_seen_FOR(self, p):
        '''seen_FOR : empty'''
        self.appendNewScope('for')

    def p_for_statement(self, p):
        '''for_statement : FOR seen_FOR '(' for_init_opt ';' expression_opt ';' for_update_opt ')' statement'''
        self.gen(p, 'for_statement')
        self.endCurrScope()

    def p_for_statement_no_short_if(self, p):
        '''for_statement_no_short_if : FOR seen_FOR '(' for_init_opt ';' expression_opt ';' for_update_opt ')' statement_no_short_if'''
        self.gen(p, 'for_statement_no_short_if')
        self.endCurrScope()

    def p_for_init_opt(self, p):
        '''for_init_opt : for_init
                        | empty'''
        self.gen(p, 'for_init_opt')

    def p_for_init(self, p):
        '''for_init : statement_expression_list
                    | local_variable_declaration'''
        self.gen(p, 'for_init')

    def p_statement_expression_list(self, p):
        '''statement_expression_list : statement_expression
                                     | statement_expression_list ',' statement_expression'''
        self.gen(p, 'statement_expression_list')

    def p_expression_opt(self, p):
        '''expression_opt : expression
                          | empty'''
        self.gen(p, 'expression_opt')

    def p_for_update_opt(self, p):
        '''for_update_opt : for_update
                          | empty'''
        self.gen(p, 'for_update_opt')

    def p_for_update(self, p):
        '''for_update : statement_expression_list'''
        self.gen(p, 'for_update')

    def p_statement_no_short_if(self, p):
        '''statement_no_short_if : statement_without_trailing_substatement
                                 | labeled_statement_no_short_if
                                 | if_then_else_statement_no_short_if
                                 | while_statement_no_short_if
                                 | for_statement_no_short_if'''
        self.gen(p, 'statement_no_short_if')

    def p_assert_statement(self, p):
        '''assert_statement : ASSERT expression ';'
                            | ASSERT expression ':' expression ';' '''
        self.gen(p, 'assert_statement')

    def p_empty_statement(self, p):
        '''empty_statement : ';' '''
        self.gen(p, 'empty_statement')

    def p_switch_statement(self, p):
        '''switch_statement : SWITCH '(' expression ')' switch_block'''
        self.gen(p, 'switch_statement')

    def p_switch_block(self, p):
        '''switch_block : '{' '}' '''
        self.gen(p, 'switch_block')

    def p_switch_block2(self, p):
        '''switch_block : '{' switch_block_statements '}' '''
        self.gen(p, 'switch_block')

    def p_switch_block3(self, p):
        '''switch_block : '{' switch_labels '}' '''
        self.gen(p, 'switch_block')

    def p_switch_block4(self, p):
        '''switch_block : '{' switch_block_statements switch_labels '}' '''
        self.gen(p, 'switch_block')

    def p_switch_block_statements(self, p):
        '''switch_block_statements : switch_block_statement
                                   | switch_block_statements switch_block_statement'''
        self.gen(p, 'switch_block_statements')

    def p_switch_block_statement(self, p):
        '''switch_block_statement : switch_labels block_statements'''
        self.gen(p, 'switch_block_statement')

    def p_switch_labels(self, p):
        '''switch_labels : switch_label
                         | switch_labels switch_label'''
        self.gen(p, 'switch_labels')

    def p_switch_label(self, p):
        '''switch_label : CASE constant_expression ':'
                        | DEFAULT ':' '''
        self.gen(p, 'switch_label')

    def p_constant_expression(self, p):
        '''constant_expression : expression'''
        self.gen(p, 'constant_expression')

    def p_do_statement(self, p):
        '''do_statement : DO statement WHILE '(' expression ')' ';' '''
        self.gen(p, 'do_statement')

    def p_break_statement(self, p):
        '''break_statement : BREAK ';'
                           | BREAK NAME ';' '''
        self.gen(p, 'break_statement')

    def p_continue_statement(self, p):
        '''continue_statement : CONTINUE ';'
                              | CONTINUE NAME ';' '''
        self.gen(p, 'continue_statement')

    def p_return_statement(self, p):
        '''return_statement : RETURN expression_opt ';' '''
        self.gen(p, 'return_statement')

    def p_class_instance_creation_expression(self, p):
        '''class_instance_creation_expression : NEW class_type '(' argument_list_opt ')' class_body_opt'''
        self.gen(p, 'class_instance_creation_expression')

    def p_class_instance_creation_expression2(self, p):
        '''class_instance_creation_expression : primary '.' NEW class_type '(' argument_list_opt ')' class_body_opt'''
        self.gen(p, 'class_instance_creation_expression')

    def p_class_instance_creation_expression3(self, p):
        '''class_instance_creation_expression : class_instance_creation_expression_name NEW class_type '(' argument_list_opt ')' class_body_opt'''
        self.gen(p, 'class_instance_creation_expression')

    def p_class_instance_creation_expression_name(self, p):
        '''class_instance_creation_expression_name : name '.' '''
        self.gen(p, 'class_instance_creation_expression_name')

    def p_class_body_opt(self, p):
        '''class_body_opt : class_body
                          | empty'''
        self.gen(p, 'class_body_opt')

    def p_field_access(self, p):
        '''field_access : primary '.' NAME'''
        self.gen(p, 'field_access')

    def p_array_access(self, p):
        '''array_access : name '[' expression ']'
                        | primary_no_new_array '[' expression ']' '''
        self.gen(p, 'array_access')

    def p_array_creation_with_array_initializer(self, p):
        '''array_creation_with_array_initializer : NEW primitive_type dim_with_or_without_exprs array_initializer
                                                 | NEW class_or_interface_type dim_with_or_without_exprs array_initializer'''
        self.gen(p, 'array_creation_with_array_initializer')

    def p_dim_with_or_without_exprs(self, p):
        '''dim_with_or_without_exprs : dim_with_or_without_expr
                                     | dim_with_or_without_exprs dim_with_or_without_expr'''
        self.gen(p, 'dim_with_or_without_exprs')

    def p_dim_with_or_without_expr(self, p):
        '''dim_with_or_without_expr : '[' expression ']'
                                    | '[' ']' '''
        self.gen(p, 'dim_with_or_without_expr')

    def p_array_creation_without_array_initializer(self, p):
        '''array_creation_without_array_initializer : NEW primitive_type dim_with_or_without_exprs
                                                    | NEW class_or_interface_type dim_with_or_without_exprs'''
        self.gen(p, 'array_creation_without_array_initializer')

class NameParser(BaseParser):

    def p_name(self, p):
        '''name : simple_name
                | qualified_name'''
        self.gen(p, 'name')
        p[0]['astName'] = 'name'

    def p_simple_name(self, p):
        '''simple_name : NAME'''
        self.gen(p, 'simple_name')
        p[0]['name'] = [p[0]['astName']]

    def p_qualified_name(self, p):
        '''qualified_name : name '.' simple_name'''
        self.gen(p, 'qualified_name')
        p[0]['name'] = p[1]['name'] + p[3]['name']

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
        p[0]['type'], p[0]['reference'] = self.find_type(p[0]['astName']), []
        if p[0]['type'] == 'error':
            print('Not a matching type at line #{}'.format(self.lexer.lineno))

    def p_literal1(self, p):
        '''literal : CHAR_LITERAL'''
        self.gen(p, 'literal')
        p[0]['type'], p[0]['reference'] = 'char', []

    def p_literal2(self, p):
        '''literal : STRING_LITERAL'''
        self.gen(p, 'literal')
        p[0]['type'], p[0]['reference'] = 'String', []

    def p_literal3(self, p):
        '''literal : TRUE
                   | FALSE'''
        self.gen(p, 'literal')
        p[0]['type'], p[0]['reference'] = 'boolean', []

    def p_literal4(self, p):
        '''literal : NULL'''
        self.gen(p, 'literal')
        p[0]['type'], p[0]['reference'] = 'null', []

class TypeParser(BaseParser):

    def p_modifiers_opt(self, p):
        '''modifiers_opt : modifiers'''
        self.gen(p, 'modifiers_opt')

    def p_modifiers_opt2(self, p):
        '''modifiers_opt : empty'''
        self.gen(p, 'modifiers_opt')

    def p_modifiers(self, p):
        '''modifiers : modifier
                     | modifiers modifier'''
        self.gen(p, 'modifiers')

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

    def p_type(self, p):
        '''type : primitive_type
                | reference_type'''
        self.gen(p, 'type')
        if p[0]['type'] !=  'primitive_type':
            p[0]['reference'] = p[0]['type']
            p[0]['type'] = 'reference'
        else:
            p[0]['type'] = p[0]['astName']

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
        p[0]['type'] = 'primitive_type'

    def p_reference_type(self, p):
        '''reference_type : class_or_interface_type
                          | array_type'''
        self.gen(p, 'reference_type')

    def p_class_or_interface_type(self, p):
        '''class_or_interface_type : class_or_interface'''
        self.gen(p, 'class_or_interface_type')
        # Not implementing generic_type

    def p_class_type(self, p):
        '''class_type : class_or_interface_type'''
        self.gen(p, 'class_type')

    def p_class_or_interface(self, p):
        '''class_or_interface : name'''
        self.gen(p, 'class_or_interface')
        p[0]['type'] = p[0]['name']

    def p_array_type(self, p):
        '''array_type : primitive_type dims
                      | name dims'''
        self.gen(p, 'array_type')
        if p[1]['astName'] == 'name':
            p[0]['type'] = p[1]['name']
        elif p[1]['type'] == 'primitive_type':
            p[0]['type'] = [p[0]['astName']]
        else:
            print('Parsing Error at line #{}'.format(self.lexer.lineno))

        p[0]['type'] += p[2]['dim']

class ClassParser(BaseParser):

    def p_type_declaration(self, p):
        '''type_declaration : class_declaration'''
        self.gen(p, 'type_declaration')

    def p_type_declaration2(self, p):
        '''type_declaration : ';' '''
        self.gen(p, 'type_declaration')

    def p_class_declaration(self, p):
        '''class_declaration : class_header class_body'''
        self.gen(p, 'class_declaration')
        self.endCurrScope()

    def p_class_header(self, p):
        '''class_header : class_header_name'''
        self.gen(p, 'class_header')

    def p_class_header_name(self, p):
        '''class_header_name : class_header_name1'''
        self.gen(p, 'class_header_name')

    def p_class_header_name1(self, p):
        '''class_header_name1 : modifiers_opt CLASS NAME'''
        self.startNewScope(p[3], 'class')
        self.gen(p, 'class_header_name1')

    def p_class_body(self, p):
        '''class_body : '{' class_body_declarations_opt '}' '''
        self.gen(p, 'class_body')

    def p_class_body_declarations_opt(self, p):
        '''class_body_declarations_opt : class_body_declarations'''
        self.gen(p, 'class_body_declarations_opt')

    def p_class_body_declarations_opt2(self, p):
        '''class_body_declarations_opt : empty'''
        self.gen(p, 'class_body_declarations_opt')

    def p_class_body_declarations(self, p):
        '''class_body_declarations : class_body_declaration
                                   | class_body_declarations class_body_declaration'''
        self.gen(p, 'class_body_declarations')

    def p_class_body_declaration(self, p):
        '''class_body_declaration : class_member_declaration
                                  | static_initializer
                                  | constructor_declaration'''
        self.gen(p, 'class_body_declaration')

    def p_class_body_declaration2(self, p):
        '''class_body_declaration : block'''
        self.gen(p, 'class_body_declaration')

    def p_class_member_declaration(self, p):
        '''class_member_declaration : field_declaration
                                    | class_declaration
                                    | method_declaration'''
        self.gen(p, 'class_member_declaration')

    def p_class_member_declaration2(self, p):
        '''class_member_declaration : ';' '''
        self.gen(p, 'class_member_declaration')

    def p_field_declaration(self, p):
        '''field_declaration : modifiers_opt type variable_declarators ';' '''
        self.gen(p, 'field_declaration')

    def p_static_initializer(self, p):
        '''static_initializer : STATIC block'''
        self.gen(p, 'static_initializer')

    def p_constructor_declaration(self, p):
        '''constructor_declaration : constructor_header method_body'''
        self.gen(p, 'constructor_declaration')
        self.endCurrScope()

    def p_constructor_header(self, p):
        '''constructor_header : constructor_header_name formal_parameter_list_opt ')' '''
        self.gen(p, 'constructor_header')
        currScope = self.symTabStack[-1]
        currScope['size'] = 0

    def p_constructor_header_name(self, p):
        '''constructor_header_name : modifiers_opt NAME '(' '''
        name = p[2]
        self.startNewScope(name, 'constructor')
        currScope = self.symTabStack[-1]
        currScope['size'] = -8
        self.gen(p, 'constructor_header_name')

    def p_formal_parameter_list_opt(self, p):
        '''formal_parameter_list_opt : formal_parameter_list'''
        self.gen(p, 'formal_parameter_list_opt')

    def p_formal_parameter_list_opt2(self, p):
        '''formal_parameter_list_opt : empty'''
        self.gen(p, 'formal_parameter_list_opt')

    def p_formal_parameter_list(self, p):
        '''formal_parameter_list : formal_parameter
                                 | formal_parameter_list ',' formal_parameter'''
        self.gen(p, 'formal_parameter_list')

    def p_formal_parameter(self, p):
        '''formal_parameter : modifiers_opt type variable_declarator_id
                            | modifiers_opt type ELLIPSIS variable_declarator_id'''

        self.gen(p, 'formal_parameter')
        # TODO Deal with Ellipsis

        currScope = self.symTabStack[-1]
        if not currScope.get('parList'):
            currScope['parList'] = {}

        # using a prefix 'var_' for all variables in symbol table
        vdid = p[3] if len(p) == 4 else p[4]
        varName = 'var_' + vdid['varName']

        p[0]['type'], p[0]['reference'] = self.resolveType(p[2], vdid)

        # Check if already declared
        # If declared, then print an error and continue, else add to symbol table
        if currScope.get(varName):
            print('Function Parameter \'{}\' at line #{} already defined in the same parameter list'.format(vdid['varName'], self.lexer.lineno))
        else:
            currScope[varName] = {}
            currScope[varName]['type'] = p[0]['type']
            currScope[varName]['lineNo'] = self.lexer.lineno

            # Alloting at-least 4 bytes to all variables passed to this function
            # TODO fix this.
            currScope[varName]['size'] = 4
            if self.gst.get(p[2]['astName']):
                if self.gst[p[2]['astName']]['desc'] == 'primitive_type':
                    currScope[varName]['size'] = max(4, self.gst[p[2]['astName']]['size'])

            # set offset for new variable(s) and update the offset value in symbol table
            # Negative offset, as according to function stack
            currScope[varName]['offset'] = currScope['size']
            currScope['size'] = currScope[varName]['offset'] - currScope[varName]['size']

            currScope[varName]['reference'] = p[0]['reference']

            # append in Parameter List
            currScope['parList'][varName] = currScope[varName]

    def p_method_body(self, p):
        '''method_body : '{' block_statements_opt '}' '''
        self.gen(p, 'method_body')

    def p_method_declaration(self, p):
        '''method_declaration : abstract_method_declaration
                              | method_header method_body'''
        self.gen(p, 'method_declaration')
        self.endCurrScope()

    def p_abstract_method_declaration(self, p):
        '''abstract_method_declaration : method_header ';' '''
        self.gen(p, 'abstract_method_declaration')

    def p_method_header(self, p):
        '''method_header : method_header_name formal_parameter_list_opt ')' method_header_extended_dims'''
        self.gen(p, 'method_header')
        currScope = self.symTabStack[-1]
        currScope['size'] = 0

    def p_method_header_name(self, p):
        '''method_header_name : modifiers_opt type NAME '(' '''
        name = p[3]
        self.startNewScope(name, 'method')
        currScope = self.symTabStack[-1]
        currScope['size'] = -8
        self.gen(p, 'method_header_name')

    def p_method_header_extended_dims(self, p):
        '''method_header_extended_dims : dims_opt'''
        self.gen(p, 'method_header_extended_dims')

    def p_argument_list_opt(self, p):
        '''argument_list_opt : argument_list'''
        self.gen(p, 'argument_list_opt')

    def p_argument_list_opt2(self, p):
        '''argument_list_opt : empty'''
        self.gen(p, 'argument_list_opt')

    def p_argument_list(self, p):
        '''argument_list : expression
                         | argument_list ',' expression'''
        self.gen(p, 'argument_list')

class CompilationUnitParser(BaseParser):

    def p_compilation_unit(self, p):
        '''compilation_unit : package_declaration'''
        self.gen(p, 'compilation_unit')

    def p_compilation_unit2(self, p):
        '''compilation_unit : package_declaration import_declarations'''
        self.gen(p, 'compilation_unit')

    def p_compilation_unit3(self, p):
        '''compilation_unit : package_declaration import_declarations type_declarations'''
        self.gen(p, 'compilation_unit')

    def p_compilation_unit4(self, p):
        '''compilation_unit : package_declaration type_declarations'''
        self.gen(p, 'compilation_unit')

    def p_compilation_unit5(self, p):
        '''compilation_unit : import_declarations'''
        self.gen(p, 'compilation_unit')

    def p_compilation_unit6(self, p):
        '''compilation_unit : type_declarations'''
        self.gen(p, 'compilation_unit')

    def p_compilation_unit7(self, p):
        '''compilation_unit : import_declarations type_declarations'''
        self.gen(p, 'compilation_unit')

    def p_compilation_unit8(self, p):
        '''compilation_unit : empty'''
        self.gen(p, 'compilation_unit')

    def p_package_declaration(self, p):
        '''package_declaration : package_declaration_name ';' '''
        self.gen(p, 'package_declaration')

    def p_package_declaration_name(self, p):
        '''package_declaration_name : modifiers PACKAGE name
                                    | PACKAGE name'''
        self.gen(p, 'package_declaration_name')

    def p_import_declarations(self, p):
        '''import_declarations : import_declaration
                               | import_declarations import_declaration'''
        self.gen(p, 'import_declarations')

    def p_import_declaration(self, p):
        '''import_declaration : single_type_import_declaration
                              | type_import_on_demand_declaration
                              | single_static_import_declaration
                              | static_import_on_demand_declaration'''
        self.gen(p, 'import_declaration')

    def p_single_type_import_declaration(self, p):
        '''single_type_import_declaration : IMPORT name ';' '''
        self.gen(p, 'single_type_import_declaration')

    def p_type_import_on_demand_declaration(self, p):
        '''type_import_on_demand_declaration : IMPORT name '.' '*' ';' '''
        self.gen(p, 'type_import_on_demand_declaration')

    def p_single_static_import_declaration(self, p):
        '''single_static_import_declaration : IMPORT STATIC name ';' '''
        self.gen(p, 'single_static_import_declaration')

    def p_static_import_on_demand_declaration(self, p):
        '''static_import_on_demand_declaration : IMPORT STATIC name '.' '*' ';' '''
        self.gen(p, 'static_import_on_demand_declaration')

    def p_type_declarations(self, p):
        '''type_declarations : type_declaration
                             | type_declarations type_declaration'''
        self.gen(p, 'type_declarations')
