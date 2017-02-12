# Instructions to run

## To extract tokens using lexer:
```
src/lexer.py <input_file>
```

## To parse a file - Generates the parse tree in "graphs" folder with the same name
```
src/parser.py <input_file>
```

## To clean the temporary files and graph
```
make clean
```

# Tests
These tests should be used:
* BinaryConverter.java
* Factorial.java
* ObjectVarsAsParameters.java
* SimpleWordCounter.java
* StringExample.java

In case you want to use more complicated testcases, you can use these (provided a 15 MB png file opens on your computer):
* EightQueens.java
* RecursionExampleDirectory.java

# Dependencies
* python2 or python3
* pydot
* ply

# Acknowledgments:
* We have modified the lexer and parser from https://github.com/musiKk/plyj.
* Graph has been generated using pydot library.
* For scanner and parser, we are using ply (python-lex-yacc).
* The tests have been taken from https://www.cs.utexas.edu/~scottm/cs307/codingSamples.htm.
