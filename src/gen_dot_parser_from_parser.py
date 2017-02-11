to_print = '''import pydot
graph = pydot.Dot(graph_type='digraph')

i = 0

def createNode(s):
    global i, graph
    p = pydot.Node(str(i), label=s)
    i += 1
    graph.add_node(p)
    return p

def gen(p, s):
    global graph
    p[0] = createNode(s)
    for i in range(1, len(p)):
        if (type(p[i]) != pydot.Node):
            p[i] = str(p[i])
            p[i] = createNode(p[i])
        graph.add_edge(pydot.Edge(p[0], p[i]))
        '''
print(to_print)

import re
from sys import argv
state = 1
index = 0
rule_lhs = ''

def printSameLine(line):
    line = line.replace('.model', 'model')
    print(line, end='')

def matchDefP(line):
    return re.search(r'def p_(.*?)\(.*?\):', line)

def handleMatch(match, line):
    global state, index, rule_lhs
    rule_lhs = match.group(1)
    index = line.index('def')
    state = 2

with open(argv[1], 'r') as f:
    for line in f:
        # print(state)
        if line.strip().startswith('#'):
            # printSameLine(line)
            pass

        elif state == 1:
            match = matchDefP(line)
            printSameLine(line)
            if match:
                handleMatch(match, line)

        elif state == 2 or state == 3:
            printSameLine(line)
            cnt = line.count('\'\'\'')
            if state == 2 and cnt == 0:
                state = 4
            state += cnt
            if state == 4:
                print(' '*(index+4) + 'gen(p, \'%s\')'%rule_lhs, end='\n\n')

        elif state == 4:
            # if re.search(r'def p_error', line):
            match = matchDefP(line)
            if line.strip().startswith(('def p_error', 'class')):
                printSameLine(line)
                state = 1
            elif match:
                printSameLine(line)
                handleMatch(match, line)
            elif re.search(r'def.*?:', line):
                printSameLine(line)
                state = 1

        else:
            printSameLine(line)

to_print = "graph.write_png('example1_graph.png')"
print(to_print)
