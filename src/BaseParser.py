import pydot

class BaseParser(object):
    def __init__(self):
        self.gst = {}
        type_size_tuples = [('boolean', 1),
                            ('void', 0),
                            ('byte', 1),
                            ('short', 2),
                            ('int', 4),
                            ('long', 8),
                            ('char', 1),
                            ('float', 4),
                            ('double', 8),
                            ('array_type', 4)] # TODO fix size of array_type
        for datatype, size in type_size_tuples:
            self.gst[datatype] = {'size': size, 'desc': 'primitive_type'}
        self.gst['desc'] = 'GLOBAL TABLE'

        self.symTabStack = [self.gst]
        self.ast = pydot.Dot(graph_type='digraph', ordering='out')
        self.ctr = 0
        self.currFile = ''

        self.intsWoLong = ['byte', 'short', 'int', 'integer']
        self.ints = self.intsWoLong + ['long']

        self.decimals = ['float', 'double']

        self.intsCharWoLong = self.intsWoLong + ['char']
        self.intsChar = self.ints + ['char']

        self.numsChar = self.intsChar + self.decimals
        self.bitwise = self.intsChar + ['boolean']

    def startNewScope(self, name, desc):
        currTable = self.symTabStack[-1]
        currTable[name] = {'size': 0, 'desc': desc}
        self.symTabStack.append(currTable[name])
        # print('Adding new Table %d %s' % (len(self.symTabStack), currTable[name]['desc']))

    def appendNewScope(self, desc):
        currTable = self.symTabStack[-1]
        if not currTable.get('blockList'):
            currTable['blockList'] = []

        newTable = {'size': 0, 'desc': desc}
        currTable['blockList'].append(newTable)
        self.symTabStack.append(newTable)

    def endCurrScope(self):
        # print('Removing a Table %d %s' % (len(self.symTabStack)-1, self.symTabStack[-1]['desc']))
        self.symTabStack.pop()

    def replace_whitespaces(self, s):
        s = s.replace('\\n', 'newline')
        s = s.replace('\\t', 'tab')
        return s

    def createNode(self, s, graph):
        s = self.replace_whitespaces(str(s))
        if '"' not in s:
            s = '"' + s + '"' # In order to avoid errors which pydot(graphviz) gives for comma, colon and some other symbols
        p = pydot.Node(str(self.ctr), label=s)
        self.ctr += 1
        graph.add_node(p)
        return p

    def gen(self, p, name, index_ast = None):
        useful_wo_index = [i for i, item in enumerate(p) if item and i != index_ast]
        useful = useful_wo_index + [index_ast] if index_ast else useful_wo_index
        if useful:
            for i in useful:
                if not isinstance(p[i], dict):
                    nodeName = p[i]
                    p[i] = {}
                    p[i]['astName'] = nodeName
                    p[i]['astNode'] = self.createNode(nodeName, self.ast)

            if len(useful_wo_index) != 1:
                if index_ast:
                    p[0] = p[index_ast]
                else:
                    p[0] = {}
                    p[0]['astName'] = name
                    p[0]['astNode'] = self.createNode(name, self.ast)
                for i in useful_wo_index:
                    self.ast.add_edge(pydot.Edge(p[0]['astNode'], p[i]['astNode']))
            else:
                p[0] = p[1]

    def recPrint(self, table, count):
        for key in table:
            if isinstance(table[key], dict):
                print('\t'*count + key)
                self.recPrint(table[key],  count+1)
            elif isinstance(table[key], list):
                for elem in table[key]:
                    if isinstance(elem, dict):
                        print('\t'*count + key)
                        self.recPrint(elem, count+1)
                    else:
                        print('\t'*count + key + '\t'*2 + str(elem))
            else:
                print('\t'*count + key + '\t'*2 + str(table[key]))

    def binary(self, p):
        return 2 if len(p) == 4 else None

    def unary(self, p):
        return 1 if len(p) == 3 else None

    def splitType(self, typeList):
        if isinstance(typeList, list):
            for i in range(0, len(typeList)):
                if type(typeList[i]) == int:
                    return typeList[:i], typeList[i:]
        return typeList, []

    def resolveType(self, varType, varName):
        if varType['type'] == 'reference':
            datatype, dim = self.splitType(varType['reference'])
        else:
            datatype = [varType['type']]
            dim = None

        if dim and varName.get('dim'):
            print('Both the Variable type and Variable name can\'t have dimension, error on line #{}'.format(self.lexer.lineno))
        else:
            dim = varName.get('dim')

        # return in the format basetype(primitive or reference), referred type(if base is not primitive), dimensions
        if not dim:
            return varType['type'], varType.get('reference')
        else:
            return 'reference', datatype + dim

    def checkTypeAssignment(self, LHS, RHS, name):
        if LHS['type'] != RHS['type']:
            if not self.convertible(RHS['type'], LHS['type']):
                print('Type mismatch at assignment operator for \'{}\' on line #{} #TODO'.format(name, self.lexer.lineno))
                print(LHS['type'], RHS['type'])
                return 0
            else:
                RHS['type'] = LHS['type']
        else:
            if (LHS['type'] == 'reference') and (RHS['type'] == 'reference'):
                datatypeL, dimL = self.splitType(LHS['reference'])
                datatypeR, dimR = self.splitType(RHS['reference'])
                # Assuming arrays of primitive_type are not convertible even if unit variables are
                if datatypeL != datatypeR and datatypeR != [0]:
                    print('Type mismatch at assignment operator for \'{}\' on line #{} #TODO'.format(name, self.lexer.lineno))
                    return 0
                else:
                    datatypeR = datatypeL
                if len(dimL) != len(dimR):
                    print('Dimensions do not match accross the assignment operator for \'{}\' at line #{}'.format(name, self.lexer.lineno))
                    return 0
        return 1

    def convertible(self, type1, type2):
        if type1 == 'reference' or type2 == 'reference' :
            return None
        else:
            # TODO
            return 1

    def findVar(self, var):
        toFind = 'var_' + var['name'][0]
        for scope in reversed(self.symTabStack):
            if scope.get(toFind):
                # TODO recurse to the actual variable
                return scope[toFind]

        print('Variable not defined {} at line #{}'.format(var['astName'], self.lexer.lineno))
        return None
