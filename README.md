Instructions to run script:

python src/gen_dot_parser_from_parser.py src/parser.py > src/parser2.py

The program generated is parser2.py which is the required parsing file with actions that add edges to the Parse tree.

To parse a file

python tmp.py test/bar.java > out.py
python out.py

Generates the parse tree in the test folder as "example1.png"
