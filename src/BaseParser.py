from __future__ import print_function
import pydot

class BaseParser(object):
    def __init__(self):
        self.gst = {}
        type_size_tuples = [('boolean',1),
                            ('void', 0),
                            ('byte', 1),
                            ('short', 2),
                            ('int', 4),
                            ('long', 8),
                            ('char', 1),
                            ('float', 4),
                            ('double', 8),
                            ('array_type', 4)]
        for type, size in type_size_tuples:
            self.gst[type] = {'size': size, 'desc': 'primitive_type'}
        self.gst['desc'] = 'GLOBAL TABLE'

        self.symTabStack = [self.gst]
        self.ptree = pydot.Dot(graph_type='digraph', ordering='out')
        self.ast = pydot.Dot(graph_type='digraph', ordering='out')
        self.ctr = 0

    def startNewScope(self, name, desc):
        currTable = self.symTabStack[-1]
        currTable[name] = {'size'   : 0,    'desc'  : desc  }
        self.symTabStack.append(currTable[name])
        # print('Adding new Table %d %s' % (len(self.symTabStack), currTable[name]['desc']))

    def appendNewScope(self, desc):
        currTable = self.symTabStack[-1]
        if not currTable.get('blockList'):
            currTable['blockList'] = []

        newTable = {'size': 0,  'desc': desc    }
        currTable['blockList'].append(newTable)
        self.symTabStack.append(newTable)
        # print('Adding new Table %d %s' % (len(self.symTabStack), newTable['desc']))

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

    def gen(self, p, s):
        p[0] = {}
        p[0]['ptreeName'] = s
        p[0]['ptreeNode'] = self.createNode(s, self.ptree)
        if len(p) != 2:
            p[0]['astName'] = s
            p[0]['astNode'] = self.createNode(s, self.ast)

        for i in range(1, len(p)):
            if not isinstance(p[i], dict):
                nodeName = p[i]
                p[i] = {}
                p[i]['ptreeName'] = nodeName
                p[i]['astName'] = nodeName
                p[i]['ptreeNode'] = self.createNode(nodeName, self.ptree)
                p[i]['astNode'] = self.createNode(nodeName, self.ast)
            self.ptree.add_edge(pydot.Edge(p[0]['ptreeNode'], p[i]['ptreeNode']))
            if len(p) != 2:
                self.ast.add_edge(pydot.Edge(p[0]['astNode'], p[i]['astNode']))
        if len(p) == 2:
            p[0]['astName'] = p[1]['astName']
            p[0]['astNode'] = p[1]['astNode']


    def recPrint(self, table, count):
        for key in table:
            if isinstance(table[key], dict):
                print('\t'*count + key)
                self.recPrint(table[key], count+1)
            else:
                print('\t'*count + key + '\t'*2 + str(table[key]))
