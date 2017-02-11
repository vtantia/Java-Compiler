import vin_parser as plyj
from sys import argv

parser = plyj.Parser()

# parse a compilation unit from a file
tree = parser.parse_file(argv[1])
