primTypeSizeTups = [('boolean', 1), ('byte', 1), ('short', 2), ('int', 4),
        ('long', 8), ('char', 1), ('float', 4), ('double', 8)]

class Type(object):
    def __init__(self, prim = True, baseType = 'int', dim = []):
        self.baseType = baseType
        self.dim = dim
        self.prim = self.isPrim()

    def isPrim(self):
        return self.dim == [] and any([self.baseType == type for type, _ in primTypeSizeTups])

    def copy(type2):
        type1 = self.type
        type2.baseType, type2.dim, type2.prim = type1.baseType, type1.dim, type1.prim

class Node(object):
    def __init__(self, astName, astNode, nodeType = Type(), qualName = []):
        self.astName = astName
        self.astNode = astNode
        self.nodeType = nodeType
        self.qualName = qualName
