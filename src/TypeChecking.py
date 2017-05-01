import Node

class TypeChecking(object):
    intsWoLong = ['integer', 'byte', 'short', 'int']
    ints = intsWoLong + ['long']

    decimals = ['float', 'double']

    intsCharWoLong = ['char'] + intsWoLong
    intsChar =  ['char'] + ints

    numsChar = intsChar + decimals
    bitwise = intsChar + ['boolean']

    def __init__(self):
        self.mapping = {'=': ('=', None),
                   '*=': ('*', self.binary_exp_addmult),
                   '/=': ('/', self.binary_exp_addmult),
                   '%=': ('%', self.binary_exp_addmult),
                   '+=': ('+', self.binary_exp_addmult),
                   '-=': ('-', self.binary_exp_addmult),
                   '<<=': ('LSHIFT', self.binary_exp_shift),
                   '>>=': ('RSHIFT', self.binary_exp_shift),
                   '>>>=': ('RRSHIFT', self.binary_exp_shift),
                   '&=': ('AND', self.binary_exp_bool),
                   '|=': ('OR', self.binary_exp_bool),
                   '^=': ('^', self.binary_exp_bitwise)
                   }

    def binary_exp_cond(self, p):
        if len(p) == 2:
            return
        if self.checkRef(p[1], p[2], p[3]):
            return

        p[0].nodeType = Node.Type(baseType='boolean')

        if p[1].nodeType.baseType != 'boolean':
            print('Incompatible type on line #{}: {}{} can\'t be converted \
                    to boolean'.format(self.lexer.lineno, p[1].nodeType.baseType, p[1].nodeType.dim))

        if p[3].nodeType == p[5].nodeType:
            p[0].nodeType = deepcopy(p[3].nodeType)
        else:
            newType = self.lca(p[3], p[5])
            if newType:
                p[0].nodeType = Type(baseType=newType)
            else:
                print('Not matching types for conditional expression at line #{}'.format(
                    self.lexer.lineno))

    def binary_exp_bool(self, p):
        if len(p) == 2:
            return

        if self.checkRef(p[1], p[2], p[3]):
            return

        p[0].nodeType = Node.Type(baseType='boolean')

        type1, type2 = p[1].nodeType.baseType, p[3].nodeType.baseType
        if type1 != 'boolean' or type2 != 'boolean':
            p[0].nodeType.baseType = 'integer'
            print('Conditional allowed only on boolean: {} at line #{}'.format(
                p[0].astName, self.lexer.lineno))

    def binary_exp_bitwise(self, p):
        if len(p) == 2:
            return

        if self.checkRef(p[1], p[2], p[3]):
            return

        type1, type2 = p[1].nodeType.baseType, p[3].nodeType.baseType
        if type1 == 'boolean' and type2 == 'boolean':
            p[0].nodeType.baseType = 'boolean'
        elif type1 in self.intsChar and type2 in self.intsChar:
            if type1 == 'long' or type2 == 'long':
                p[0].nodeType.baseType = 'long'
            else:
                p[0].nodeType.baseType = 'int'
        else:
            p[0].nodeType.baseType = 'int'
            print('Incompatible types around the operator {} at line #{}'.format(
                p[2].astName, self.lexer.lineno))

    def binary_exp_rel(self, p):
        if len(p) == 2:
            return

        if self.checkRef(p[1], p[2], p[3]):
            return

        p[0].nodeType.baseType = 'boolean'

        type1, type2 = p[1].nodeType.baseType, p[3].nodeType.baseType
        oper = p[2].astName
        if oper == 'instanceof':
            pass
        elif type1 == type2 or self.checkTypeAssignment(p[1], p[3]):
            # TODO Think about the above Condition
            if type1 in self.numsChar:
                pass
            elif (oper == '==' or oper == '!=') and type1 == 'boolean':
                pass
            else:
                print('Incompatible operator {} with boolean type line #{}'.format(
                    oper, self.lexer.lineno))
        else:
            print('Not matching types for {} at line #{}'.format(p[0].astName, self.lexer.lineno))

    def binary_exp_shift(self, p):
        if len(p) == 2:
            return

        if self.checkRef(p[1], p[2], p[3]):
            return

        type1, type2 = p[1].nodeType.baseType, p[3].nodeType.baseType
        if type1 in self.intsChar and type2 in self.intsChar:
            p[0].nodeType.baseType = 'long' if (type1 == 'long' or type2 == 'long') else 'int'
        else:
            p[0].nodeType.baseType = 'int'
            print('Not matching types for {} at line #{}'.format(p[0].astName, self.lexer.lineno))

    def binary_exp_addmult(self, p):
        if len(p) == 2:
            return

        if self.checkRef(p[1], p[2], p[3]):
            return

        type1, type2 = p[1].nodeType.baseType, p[3].nodeType.baseType

        if p[0].astName != '%':
            if type1 in self.numsChar and type2 in self.numsChar:
                for type in ['double', 'float', 'long']:
                    if type1 == type or type2 == type:
                        p[0].nodeType.baseType = type
                        break
                else:
                    p[0].nodeType.baseType = 'int'
            elif p[2].astName == '+' and (type1 == "String" or type2 == "String"):
                p[0].nodeType.baseType = 'String'
            else:
                p[0].nodeType.baseType = 'int'
                print('Not matching types for {} at line #{}'.format(
                    p[0].astName, self.lexer.lineno))
        else:
            self.binary_exp_shift(p)

    def unary_exp_nots(self, p):
        if len(p) == 2:
            return

        if self.checkRef(p[2], p[1]):
            return

        if p[0].astName == '~':
            p[0].nodeType.baseType = 'int'
            if p[2].nodeType.baseType in self.intsCharWoLong:
                pass
            elif p[2].nodeType.baseType == 'long':
                p[0].nodeType.baseType = 'long'
            else:
                print('Not a matching type for ~ at line #{}'.format(
                    self.lexer.lineno))

        if p[0].astName == '!':
            p[0].nodeType.baseType = 'boolean'
            if p[2].nodeType.baseType != 'boolean':
                print('Not a matching type for ! at line #{}'.format(
                    self.lexer.lineno))

    def unary_exp_post(self, p, index):
        if len(p) == 2:
            return

        if self.checkRef(p[index], p[3-index]):
            return

        p[0].nodeType.baseType = p[index].nodeType.baseType
        if p[index].nodeType.baseType not in self.numsChar:
            print('Type error in post expression at line # {}'.format(self.lexer.lineno))

    def unary_exp_plus(self, p):
        if len(p) == 2:
            return

        if self.checkRef(p[2], p[1]):
            return

        if p[0].astName in ['+', '-']:
            if p[1].nodeType.baseType in self.intsCharWoLong:
                p[0].nodeType.baseType = 'int'
            elif p[1].nodeType.baseType in self.decimals + ['long']:
                p[0].nodeType.baseType = p[2].nodeType.baseType
            else:
                p[0].nodeType.baseType = 'int'
                print('Not a matching type for {} at line #{}'.format(
                    p[0].astName, self.lexer.lineno))

    def checkRef(self, p1, p2, p3 = None):
        isPrim1 = p1.isPrim() or p1.nodeType.baseType == "String"
        isPrim3 = p3 is None or p3.isPrim() or p3.nodeType.baseType == "String"
        if isPrim1 and isPrim3:
            return False
        else:
            #  print(isPrim1, isPrim3)
            #  print(p1.astName, p3.astName)
            #  print('Incompatible type on line #{}: {} {} for operation {}'.
                    #  format(self.lexer.lineno, p1.nodeType.baseType,
                        #  'and ' + p3.nodeType.baseType if p3 else '', p2.astName))
            return True

    def binary(self, p):
        return 2 if len(p) == 4 else None

    def unary(self, p):
        return 1 if len(p) == 3 else None

    def lca(self, t1, t2):
        assert type(t1) is Node.Type and type(t2) is Node.Type

        a, b = t1.baseType, t2.baseType
        idx = max(self.numsChar.index(a), self.numsChar.index(b))

        # If only one of them is char and the other is not integer - to
        # handle cases like byte, char and short, char
        if [a,b].count('char') == 1 and [a,b].count('integer') == 0:
            idx = max(idx, self.numsChar.index(int))

        return self.numsChar[idx]

    def checkTypeAssignment(self, LHS, RHS, ifNode=True):
        if ifNode:
            assert type(LHS) is Node.Node and type(RHS) is Node.Node
            a, b = LHS.nodeType, RHS.nodeType

        else:
            assert type(LHS) is Node.Type and type(RHS) is Node.Type
            a, b = LHS, RHS

        if len(a.dim) != len(b.dim):
            flag, err = False, "Dimension mismatch error"

        # TODO Discuss
        elif b.dim[1:].count(0) == len(b.dim[1:]) and b.dim[1:]:
            flag, err = False, "Multidimensional array on RHS needs unit size"

        else:
            a.dim = b.dim
            if a.baseType == b.baseType:
                flag, finalType = True, a.baseType
            elif self.lca(a,b) == a.baseType:
                flag, finalType = True, a.baseType
            else:
                flag, err = False, "Base type mismatch error"

        if flag:
            return finalType
        else:
            print(err, 'at assignment operator on line #{}'.format(self.lexer.lineno))
            return False

    def assign(self, tup, p):
        op, func = tup
        if op != '=':
            tmp = p[2].astName
            p[2].astName = op
            func(p)
            self.checkTypeAssignment(p[1], p[0])
            p[2].astName = tmp
        else:
            self.checkTypeAssignment(p[1], p[3])
