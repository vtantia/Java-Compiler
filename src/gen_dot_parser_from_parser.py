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

def printSameLine(line):
    line = line.replace('.model', 'model')
    print(line, end='')

def matchDefP(line):
    return re.search(r'def p_(.*?)\(.*?\):', line)

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
                s = match.group(1)
                state = 2

        elif state == 2 or state == 3:
            printSameLine(line)
            cnt = line.count('\'\'\'')
            if state == 2 and cnt == 0:
                state = 4
            state += cnt
            if state == 4:
                print('        gen(p, \'%s\')'%s, end='\n\n')

        elif state == 4:
            # if re.search(r'def p_error', line):
            match = matchDefP(line)
            if line.strip().startswith(('def p_error', 'class')):
                printSameLine(line)
                state = 1
            elif match:
                printSameLine(line)
                s = match.group(1)
                state = 2
            elif re.search(r'def.*?:', line):
                printSameLine(line)
                state = 1

        else:
            printSameLine(line)

to_print = "graph.write_png('example1_graph.png')"
print(to_print)
