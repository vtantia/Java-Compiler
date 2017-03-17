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
        parserObj.recPrint(parserObj.gst, 0) # TODO

        if len(argv) == 4:
            out_file = argv[2]
            out_file = out_file.replace('tests/','graphs/')
            out_file = out_file.replace('.java','.png')
            out_file_ast = out_file.replace('.png','_ast.png')
            dir = 'graphs'
            if not os.path.exists(dir):
                os.makedirs(dir)
            parserObj.ptree.write_png(out_file)
            parserObj.ast.write_png(out_file_ast)
            print('Parse tree output in file \'{}\''.format(out_file))

    else:
        print('No such option \'{}\''.format(argv[1]))
