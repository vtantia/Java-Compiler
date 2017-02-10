s = '''import pydot
graph = pydot.Dot(graph_type='digraph')

i = 0

def createNode(s):
    global i
    p = pydot.Node(str(i), label=s)
    i += 1
    graph.add_node(p)
    return p

def gen(p, s):
    p[0] = createNode(s)
    for i in range(1,len(p)):
        if (type(p[i]) != pydot.Node):
            p[i] = createNode(p[i])
        graph.add_edge(pydot.Edge(p[0],p[i]))
        '''
print(s)

import re
from sys import argv
state = 1

with open(argv[1], 'r') as f:
    for line in f:
        # print(state)

        if state == 1:
            match = re.search(r'def p_(.*?)\(.*?\):', line)
            print(line, end='')
            if match:
                s = match.group(1)
                state = 2

        elif state == 2 or state == 3:
            print(line, end='')
            cnt = line.count('\'\'\'')
            if state == 2 and cnt == 0:
                state = 4
            state += cnt
            if state == 4:
                print('        gen(p, \'%s\')'%s, end='\n\n')

        elif state == 4:
            if re.search(r'def p_error', line):
                print(line, end = '')
                state = 5
                continue
            match = re.search(r'def p_(.*?)\(.*?\).*?:', line)
            if match:
                print(line, end = '')
                s = match.group(1)
                state = 2
            elif re.search(r'def.*?:', line):
                print(line, end = '')
                state = 1

        else:
            print(line, end = '')

s = "graph.write_png('example1_graph.png')"
print(s)
