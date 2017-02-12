all:
	$(info To run, follow the instructions in README.md)

clean:
	rm -rf src/__pycache__
	rm -f src/parsetab.py src/lextab.py src/parser.out src/*.pyc
