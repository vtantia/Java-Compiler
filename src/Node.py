primTypeSize = [('boolean', 1), ('byte', 1), ('short', 2), ('int', 4),
        ('long', 8), ('char', 1), ('float', 4), ('double', 8)]

class Type(object):
    def __init__(self, isPrim = True, baseType = 'int', dim = []):
        self.isPrim = isPrim
        self.baseType = baseType
        self.dim = dim

    def isPrim(self):
        return any([self.baseType == type for type, _ in types])

class Node(object):
    def __init__(self, astName, astNode, nodeType = Type(), qualName = []):
        self.astName = astName
        self.astNode = astNode
        self.nodeType = nodeType
        self.qualName = qualName
