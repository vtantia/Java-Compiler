intsWoLong = ['byte', 'short', 'int', 'integer']
ints = intsWoLong + ['long']

decimals = ['float', 'double']

intsCharWoLong = intsWoLong + ['char']
intsChar = ints + ['char']

numsChar = intsChar + decimals
bitwise = intsChar + ['boolean']

def binary_exp_cond(p):
    if len(p) == 2:
        return


    p[0]['type'], p[0]['reference'] = 'boolean', []

    if p[1]['type'] != 'boolean':
        print('Incompatible type on line #{}: {} {} can\'t be converted \
                to boolean'.format(self.lexer.lineno, p[1]['type'], p[1]['reference']))

    if p[3]['type'] == p[5]['type'] and p[3]['reference'] == p[5]['reference']:
        p[0]['type'], p[0]['reference'] = p[3]['type'], p[3]['reference']
    else:
        # TODO fix this
        newType = self.checkTypeAssignment(p[3], p[5])
        if newType:
            p[0].nodeType = Type(isPrim = baseType = newType)
            p[0]['type'] = newType
            p[0]['reference'] = []
        else:
            print('Not matching types for conditional expression at line #{}'.format(
                self.lexer.lineno))


def binary_exp_bool(p):
    if len(p) == 2:
        return

    if p[1]['astName'] == 'name':
        p[1]['astName'] = p[1]['name']
        symTabEntry = self.findVar(p[1])
        p[1]['type'], p[1]['reference'] = symTabEntry['type'], symTabEntry['reference']

    p[0]['type'], p[0]['reference'] = 'boolean', []

    type1, type2 = p[1]['type'], p[3]['type']
    if type1 != 'boolean' and type2 != 'boolean':
        print('Conditional allowed only on boolean: {} at line #{}'.format(
            p[0]['astname'], self.lexer.lineno))


def binary_exp_bitwise(p):
    if len(p) == 2:
        return

    if p[1]['astName'] == 'name':
        p[1]['astName'] = p[1]['name']
        symTabEntry = self.findVar(p[1])
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

def binary_exp_rel(p):
    if len(p) == 2:
        return

    if p[1]['astName'] == 'name':
        p[1]['astName'] = p[1]['name']
        symTabEntry = self.findVar(p[1])
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

def binary_exp_shift(p):
    if len(p) == 2:
        return

    if p[1]['astName'] == 'name':
        p[1]['astName'] = p[1]['name']
        symTabEntry = self.findVar(p[1])
        p[1]['type'], p[1]['reference'] = symTabEntry['type'], symTabEntry['reference']

    type1, type2 = p[1]['type'], p[3]['type']
    if type1 in self.intsChar and type2 in self.intsChar:
        p[0]['type'] = 'long' if (type1 == 'long' or type2 == 'long') else 'int'
        p[0]['reference'] = []
    else:
        p[0]['type'], p[0]['reference'] = 'int', []
        print('Not matching types for {} at line #{}'.format(p[0]['astName'], self.lexer.lineno))

def binary_exp_addmult(p):
    if len(p) == 2:
        return

    if p[1]['astName'] == 'name':
        p[1]['astName'] = p[1]['name']
        symTabEntry = self.findVar(p[1])
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

def unary_exp_nots(p):
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

def unary_exp_post(p, index):
    p[0]['type'], p[0]['reference']= p[index]['type'], []
    if p[index]['type'] not in self.numsChar:
        print('Type error in post expression at line # {}'.format(self.lexer.lineno))

def unary_exp_plus(p):
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

def binary(p):
    return 2 if len(p) == 4 else None

def unary(p):
    return 1 if len(p) == 3 else None
