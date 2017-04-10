primTypeSizeTups = [('boolean', 1), ('byte', 1), ('short', 2), ('int', 4),
        ('long', 8), ('char', 1), ('float', 4), ('double', 8)]

class Type(object):
    def __init__(self, baseType = 'integer', dim = []):
        self.baseType = baseType
        self.dim = dim
        self.prim = self.isPrim()

    def isPrim(self):
        return self.dim == [] and any([self.baseType == type for type, _ in primTypeSizeTups])

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class Node(object):
    def __init__(self, astName, astNode, nodeType = None, qualName = []):
        self.astName = astName
        self.astNode = astNode
        self.nodeType = nodeType if nodeType is not None else Type()
        self.qualName = qualName

    def isPrim(self):
        return self.nodeType.isPrim()
