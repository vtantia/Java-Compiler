from copy import deepcopy

primTypeSizeTups = [('boolean', 1), ('byte', 1), ('short', 2), ('int', 4),
        ('long', 8), ('char', 1), ('float', 4), ('double', 8)]


class Type(object):
    def __init__(self, baseType='integer', dim=[]):
        self.baseType = baseType
        self.dim = dim
        self.prim = self.isPrim()

    def isPrim(self):
        return self.dim == [] and any(
                [self.baseType == type for type, _ in primTypeSizeTups]
                + [self.baseType == 'integer'])

        def __eq__(self, other):
            return self.__dict__ == other.__dict__


class Node(object):
    def __init__(self, astName, astNode, nodeType=None, qualName=[],
            tacLists=None, temporary = ''):
        self.astName = astName
        self.astNode = astNode
        self.nodeType = nodeType if nodeType is not None else Type()
        self.qualName = qualName
        self.tacLists = tacLists if tacLists is not None else TacLists()
        self.temporary = temporary # To store the temporary in which this node is present
        self.reference = None

    def isPrim(self):
        return self.nodeType.isPrim()


class TacLists(object):
    def __init__(self, nextList=[], trueList=[], falseList=[],
            contList=[], brkList=[], returnList=[]):
        self.nextList = nextList
        self.trueList = trueList
        self.falseList = falseList
        self.contList = contList
        self.brkList = brkList

    def __add__(self, other):
        newLists = deepcopy(self)
        newLists.nextList += other.nextList
        newLists.trueList += other.trueList
        newLists.falseList += other.falseList
        newLists.contList += other.contList
        newLists.brkList += other.brkList

        return newLists
