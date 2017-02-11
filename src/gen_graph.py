import final_parser
from sys import argv

parser = final_parser.Parser()

# parse a compilation unit from a file
tree = parser.parse_file(argv[1])
