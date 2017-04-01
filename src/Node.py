class Type(object):
    def __init__(self, isPrim = True, baseType = 'int', dim = []):
        self.isPrim = isPrim
        self.baseType = baseType
        self.dim = dim

class Node(object):
    def __init__(self, astName, astNode, nodeType = Type(), qualName = []):
        self.astName = astName
        self.astNode = astNode
        self.nodeType = nodeType
        self.qualName = qualName
