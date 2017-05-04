import pydot
import Node
from TypeChecking import TypeChecking
from copy import deepcopy
from ThreeAddressCode import ThreeAddressCode
from Temp import Temp


class BaseParser(TypeChecking):
    def __init__(self):
        TypeChecking.__init__(self)
        self.gst = {}
        typeSizeTups = Node.primTypeSizeTups + [('void', 0)]
        for datatype, size in typeSizeTups:
            self.gst[datatype] = {'size': size, 'desc': 'primitive_type'}
        self.gst['desc'] = 'GLOBAL TABLE'

        self.symTabStack = [self.gst]
        self.ast = pydot.Dot(graph_type='digraph', ordering='out')
        self.tac = ThreeAddressCode(self)
        self.ctr = 0
        self.currFile = ''
        self.curTempCnt = 0

    def startNewScope(self, name, desc):
        currTable = self.symTabStack[-1]
        if not currTable.get(name):
            currTable[name] = {
                    'size': -4 if desc == 'class' else 0,
                    'desc': desc,
                    'scope_name': name,
                    'blockList': []}

        # allow abstract declaration for method
        elif desc != 'method':
            print('Multiple definitions for {} {} defined on line #{}'.format(
                desc, name, self.lexer.lineno))

        self.symTabStack.append(currTable[name])
        # print('Adding new Table %d %s' % (len(self.symTabStack), currTable[name]['desc']))

    def appendNewScope(self, desc):
        currTable = self.symTabStack[-1]

        newTable={
            'size': currTable['size'],
            'desc': desc,
            'blockList': []}

        currTable['blockList'].append(newTable)
        self.symTabStack.append(newTable)

    def endCurrScope(self):
        # print('Removing a Table %d %s' % (len(self.symTabStack)-1,
            # self.symTabStack[-1]['desc']))
        currTable=self.symTabStack[-1]

        if currTable['desc'] == 'class':
            currTable['size'] += 4

        maxOffset=currTable['size']
        for block in currTable['blockList']:
            maxOffset=max(maxOffset, block['size'])

        currTable['size']=maxOffset

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

    def makeMarkerNode(self):
        return Node.Node('marker', self.createNode('marker'))

    def gen(self, p, name, index_ast=None):
        useful_wo_index = [i for i, item in enumerate(p) if item and i != index_ast]
        useful = useful_wo_index + [index_ast] if index_ast else useful_wo_index
        if useful:
            for i in useful:
                if not isinstance(p[i], Node.Node):
                    nodeName = p[i]
                    p[i] = Node.Node(nodeName, self.createNode(nodeName))

            if len(useful) != 1:
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
            elif isinstance(table[key], Node.Type):
                print('\t'*count + key)
                print('\t'*(count+1) + 'type' + '\t'*2 + table[key].baseType)
                print('\t'*(count+1) + 'dim' + '\t'*2 + str(table[key].dim))
            else:
                print('\t'*count + key + '\t'*2 + str(table[key]))

    def resolveType(self, varType, varName):
        t1 = varType.nodeType
        t2 = varName.nodeType

        typeParent = deepcopy(varType.nodeType)

        if t1.dim and t2.dim:
            print('Both the Variable type and Variable name can\'t  have dimension, error on line #{}'.
                    format(self.lexer.lineno))

        if not t1.dim:
            typeParent.dim = t2.dim

        return typeParent

    # Returns symbol table entry for qualified name
    def findVar(self, var):
        toFind = var[0]
        err = False

        for scope in reversed(self.symTabStack):
            if scope.get(toFind):
                varEntry = scope[toFind]
                break
        else:
            print('Variable {} on line #{} not found'.format(toFind, self.lexer.lineno))
            err = True

        if not err:
            for i in range(1, len(var)):
                varType = varEntry['type']
                currScope = self.gst.get(varType.baseType)

                if varType.dim:
                    print('Variable {} on line #{} is of array_type'.format(
                        var[i-1], self.lexer.lineno))
                    err = True
                    break

                if currScope is None:
                    print('{} on line #{} not a valid base type'.format(
                        varType.baseType, self.lexer.lineno))
                    err = True
                    break
                elif currScope.get(var[i]):
                    varEntry = currScope[var[i]]
                else:
                    print('{} on line #{} is not a valid member of {}'.format(
                        var[i], self.lexer.lineno, varType.baseType))
                    err = True
                    break

        if err:
            return None
        else:
            return varEntry

    def resolveScope(self, var):
        if var.astName == 'name':
            var.astName = var.qualName[0]
            symTabEntry = self.findVar(var.qualName)
            if symTabEntry:
                var.nodeType = symTabEntry['type']
                var.temporary = self.allotNewTemp()
                self.tac.emit('lw', var.temporary, str(-symTabEntry['offset']) + '($30)' )
                var.offset = symTabEntry['offset']

    def checkMethodInvocation(self, func, f_name, argList):

        if not func:
            return False

        desc = func.get('desc')
        parList = func.get('parList')
        if not parList:
            parList = []
        if desc != 'method' and desc != 'constructor':
            print('On line #{}, {} is not a function'.format(
                self.lexer.lineno, f_name))
            return False
        elif len(parList) == len(argList):
            for i in range(0, len(parList)):

                expected_type = func[parList[i]]['type']
                argument_type = argList[i]

                if not self.checkTypeAssignment(expected_type, argument_type, ifNode=False):

                    print('Incompatible argument type passed to method {} at line #{}'.
                            format(f_name, self.lexer.lineno))
                    print('for parameter {}, Expected type: {} {}, argument type: {} {}'.
                        format(parList[i], expected_type.baseType, len(expected_type.dim),
                                argument_type.baseType, len(argument_type.dim)))

            return func['type']
        else:
            print('method {} requires {} arguments, passed {} on line #{}'.
                    format(f_name, len(func['parList']), len(argList), self.lexer.lineno))

            return False

    def findAttribute(self, node_type, attribute):
        err=False

        if node_type.dim:
            print('Can\'t dereference {} on line #{} from array_type'.format(
                attribute, self.lexer.lineno))
            err = True

        currScope = self.gst.get(node_type.baseType)

        if currScope and currScope.get(attribute):
            varEntry = currScope[attribute]
        else:
            print('{} on line #{} is not a valid member of {}'.format(
                attribute, self.lexer.lineno, node_type.baseType))
            err = True

        if err:
            return False
        else:
            return varEntry

    # Following functions are common to both method and constructor
    def startNewMethodDef(self, name, retType):
        currScope = self.symTabStack[-1]
        currScope['type'] = retType
        currScope['size'] = -12
        currScope['funcLabel'] = self.tac.getLabelFunc(name)

    def startNewMethodDef2(self):
        currScope = self.symTabStack[-1]

        currScope['sizeParams'] = -currScope['size'] - 8
        currScope['size'] = 0

        # Push return address, save bp and copy sp to bp
        self.tac.emit('subi', '$sp', '$sp', 8)
        self.tac.emit('sw', '$31', '4($sp)')
        self.tac.emit('sw', '$30', '($sp)')
        self.tac.emit('move', '$30', '$sp')

        # Will be later patched when the size is computed
        # stack offset for this method's local variable
        currScope['sizePatch'] = self.tac.nextquad()
        self.tac.emit('subi', '$sp', '$sp')

    def getMainSize(self):
        flag = False
        mainSize = 0

        for key in self.gst:
            if isinstance(self.gst[key], dict) and self.gst[key].get('main'):
                if flag:
                    print('Multiple main functions defined')

                flag = True
                mainSize = self.gst[key]['size']

        return mainSize

    def allotNewTemp(self):
        self.curTempCnt += 1
        temp = Temp(self.curTempCnt, self.symTabStack[-1])
        return temp #'t' + str(self.curTempCnt)
