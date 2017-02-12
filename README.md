# Instructions to run

## To extract tokens using lexer:
```
src/lexer.py <input_file>
```

## To parse a file - Generates the parse tree in "graphs" folder
```
src/parser.py <input_file>
```

## To clean the temporary files and graph
```
make clean
```

# Dependencies
* python2 or python3
* pydot
* ply

# Acknowledgments:
* We have modified the lexer and parser from https://github.com/musiKk/plyj.
* Graph has been generated using pydot library.
* For scanner and parser, we are using ply (python-lex-yacc).
