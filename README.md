Instructions to generate almost complete parser:

python old/gen_dot_parser_from_parser.py old/parser.py > src/almost_complete_parser.py

The program generated is almost_complete_parser.py which is the required parsing file with actions that add edges to the Parse tree.

To parse a file

cd src
make

Generates the parse tree in the test folder as "graph.png"
