import re
from sys import argv
state = 1
index = 0


def printSameLine(line):
    line = line.replace('.model', 'model')
    print(line, end='')


def matchDefP(line):
    return re.search(r'def p_(.*?)\(.*?\):', line)


def handleMatch(match, line):
    global state, index, rule_lhs
    index = line.index('def')
    state = 2

with open(argv[1], 'r') as f:
    for line in f:
        # print(state)
        if line.strip().startswith('#'):
            printSameLine(line)
            pass

        elif state == 1:
            match = matchDefP(line)
            printSameLine(line)
            if match:
                handleMatch(match, line)

        elif state == 2:
            # if re.search(r'def p_error', line):
            match = matchDefP(line)
            if line.strip().startswith('class '):
                state = 1
            elif match:
                handleMatch(match, line)

            if state != 2 or match:
                print(' '*(index+4)+'if p[0]:')
                print(' '*(index+8)+'p[0].codeEnd = self.TAC.nextquad()\n')

            printSameLine(line)

        else:
            printSameLine(line)
