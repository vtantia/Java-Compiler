from collections import defaultdict
import pydot

class BaseParser(object):
    def __init__(self):
        self.gst = defaultdict(lambda: [])
        type_size_tuples = [('boolean', 1),
                            ('void', 0),
                            ('byte', 1),
                            ('short', 2),
                            ('int', 4),
                            ('long', 8),
                            ('char', 1),
                            ('float', 4),
                            ('double', 8),
                            ('array_type', 4)]
        for datatype, size in type_size_tuples:
            self.gst[datatype].append({'size': size, 'desc': 'primitive_type'})
        self.gst['desc'] = 'GLOBAL TABLE'

        self.symTabStack = [self.gst]
        self.ptree = pydot.Dot(graph_type='digraph', ordering='out')
        self.ast = pydot.Dot(graph_type='digraph', ordering='out')
        self.ctr = 0

    def newTable(self, desc):
        dict = {'size':0, 'desc':desc}
        return defaultdict(lambda: [], dict)

    def startNewScope(self, name, desc):
        currTable = self.symTabStack[-1]
        newTable = self.newTable(desc)
        currTable[name].append(newTable)
        self.symTabStack.append(newTable)
        # print('Adding new Table %d %s' % (len(self.symTabStack), currTable[name]['desc']))

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
        useful = [i for i, item in enumerate(p) if item is not None]
        if useful:
            p[0] = {}
            p[0]['ptreeName'] = s
            p[0]['ptreeNode'] = self.createNode(s, self.ptree)

            if len(useful) != 1:
                p[0]['astName'] = s
                p[0]['astNode'] = self.createNode(s, self.ast)

            for i in useful:
                if not isinstance(p[i], dict):
                    nodeName = p[i]
                    p[i] = {}
                    p[i]['ptreeName'] = nodeName
                    p[i]['astName'] = nodeName
                    p[i]['ptreeNode'] = self.createNode(nodeName, self.ptree)
                    p[i]['astNode'] = self.createNode(nodeName, self.ast)
                self.ptree.add_edge(pydot.Edge(p[0]['ptreeNode'], p[i]['ptreeNode']))
                if len(useful) != 1:
                    self.ast.add_edge(pydot.Edge(p[0]['astNode'], p[i]['astNode']))
            if len(useful) == 1:
                p[0]['astName'] = p[1]['astName']
                p[0]['astNode'] = p[1]['astNode']

    def recPrint(self, table, count):
        for key in table:
            if isinstance(table[key], list):
                for elem in table[key]:
                    if isinstance(elem, defaultdict):
                        print('\t'*count + key)
                        self.recPrint(elem, count+1)
                    else:
                        print('\t'*count + key + '\t'*2 + str(elem))
            else:
                print('\t'*count + key + '\t'*2 + str(table[key]))
