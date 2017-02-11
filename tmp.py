import src.parser3 as plyj
from sys import argv

parser = plyj.Parser()

print('import pydot')
print('G = pydot.Dot(graph_type=\'digraph\')')

# parse a compilation unit from a file
tree = parser.parse_file(argv[1])

print('G.write_png(\'example1.png\')')
