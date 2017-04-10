import pydot
import Node
from TypeChecking import TypeChecking
from copy import deepcopy

class BaseParser(TypeChecking):
    def __init__(self):
        self.gst = {}
        typeSizeTups = Node.primTypeSizeTups + [('void', 0)]
        for datatype, size in typeSizeTups:
            self.gst[datatype] = {'size': size, 'desc': 'primitive_type'}
        self.gst['desc'] = 'GLOBAL TABLE'

        self.symTabStack = [self.gst]
        self.ast = pydot.Dot(graph_type='digraph', ordering='out')
        self.ctr = 0
        self.currFile = ''


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

    def createNode(self, s):
        s = self.replace_whitespaces(str(s))
        if '"' not in s:
            s = '"' + s + '"' # In order to avoid errors which pydot(graphviz) gives for comma, colon and some other symbols
        p = pydot.Node(str(self.ctr), label=s)
        self.ctr += 1
        self.ast.add_node(p)
        return p

    def gen(self, p, name, index_ast = None):
        useful_wo_index = [i for i, item in enumerate(p) if item and i != index_ast]
        useful = useful_wo_index + [index_ast] if index_ast else useful_wo_index
        if useful:
            for i in useful:
                if not isinstance(p[i], Node.Node):
                    nodeName = p[i]
                    p[i] = Node.Node(nodeName, self.createNode(nodeName))

            if len(useful_wo_index) != 1:
                if index_ast:
                    p[0] = p[index_ast]
                else:
                    p[0] = Node.Node(name, self.createNode(name))
                for i in useful_wo_index:
                    self.ast.add_edge(pydot.Edge(p[0].astNode, p[i].astNode))
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

    def resolveType(self, varType, varName):
        t1 = varType.nodeType
        t2 = varName.nodeType
        if t1.dim and t2.dim:
            print('Both the Variable type and Variable name can\'t have dimension, error on line #{}'.format(self.lexer.lineno))

        typeParent = deepcopy(varType.nodeType)
        if not t1.dim:
            typeParent.dim = t2.dim

        return typeParent

    def findVar(self, var, isString = False):
        if isString:
            toFind = var
        else:
            toFind = var.qualName[0]
        for scope in reversed(self.symTabStack):
            if scope.get(toFind):
                # TODO recurse to the actual variable
                return scope[toFind]

        print('Variable {} at line #{} not defined'.format(toFind, self.lexer.lineno))
        return None

    def resolveScope(self, var):
        if var.astName == 'name':
            var.astName = var.qualName[0]
            symTabEntry = self.findVar(var)
            var.nodeType = symTabEntry['type']
