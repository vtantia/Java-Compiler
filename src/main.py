#!/usr/bin/python3

from sys import argv
import os

from PLYParser import Parser

def handle_errors(argv):
    if len(argv) < 3:
        print('To run script: src/parser.py <mode> <path_to_file> ')
        exit()

    if argv[2].find('.java') == -1:
        print('\'{}\' is not a .java file'.format(argv[2]))
        exit()
    elif not os.path.isfile(argv[2]):
        print('file \'{}\' does not exists'.format(argv[2]))
        exit()

def makeExecutable(data, code, labelMap, mallocSize):
    print(labelMap)
    revMap = {}
    for label in labelMap:
        line = labelMap[label]
        if not revMap.get(line):
            revMap[line] = []

        revMap[line] += [label]

    prefixCode1 = [['li', '$v0', 9, None],
                ['li', '$a0', mallocSize, None],
                ['syscall', 'None', 'None', 'None'],
                ['subi', '$sp', '$sp', 4],
                ['sw', '$v0', '($sp)', None]]

    prefixCode2 = [['subi', '$sp', '$sp', 4],
                ['sw', '$0', '($sp)', None]]

    callCode = [['jal', 'main0', None, None],
                ['nop', None, None, None],
                ['li', '$v0', 10, None],
                ['syscall', None, None, None]]

    code = callCode + code
    if mallocSize:
        i = -9
        code = prefixCode1 + code
    else:
        i = -6
        code = prefixCode2 + code

    revMap[i] = ['__start']

    # Printing data section
    if (data):
        print('.data')
        for item in data:
            print(item)

    # Printing code
    print('.text')
    for line in code:
        if revMap.get(i):
            for label in revMap[i]:
                print(label + ':    ')

        print('\t\t', end='')
        for unit in line:
            if unit is not None:
                print(unit, end='\t')

        i += 1
        print()

if __name__=="__main__":
    # initialize Parser
    parser = Parser()
    handle_errors(argv)

    # for Tokenizing a file
    if argv[1] == '-l':
        parser.tokenize_file(argv[2])
        exit()

    elif argv[1] == '-p':
        tree = parser.parse_file(argv[2])

        parserObj = parser.parserObj
        #  parserObj.recPrint(parserObj.gst, 0)

        makeExecutable(parserObj.tac.data, parserObj.tac.code,
                parserObj.tac.labelMap, parserObj.getMainSize())
        #  for item in parserObj.tac.data:
            #  print(item)
        #  for item in parserObj.tac.code:
            #  print(item)

        if len(argv) == 4:
            out_file = argv[2]
            out_file = out_file.replace('tests/','graphs/')
            out_file = out_file.replace('.java','.png')
            dir = 'graphs'
            if not os.path.exists(dir):
                os.makedirs(dir)
            parserObj.ast.write_png(out_file)
            print('AST output in file \'{}\''.format(out_file))

    else:
        print('No such option \'{}\''.format(argv[1]))
