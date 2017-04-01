from Node import Node

def convertible(type1, type2):
    if type1 == 'reference' or type2 == 'reference' :
        return None
    else:
        # TODO
        return 1

def allZeros(arr):
    return arr.count(0) == len(arr)

def matchType(a, b, assign = True):
    assert type(a) is Node and type(b) is Node

    a = a.nodeType
    b = b.nodeType

    if not ((a.dim == b.dim) or 
            (len(a.dim) == len(b.dim) and 
                (self.allZeros(a.dim) or self.allZeros(b.dim)))):
        return False, "Dimension mismatch error"
    if a.baseType != b.baseType:
        
        return False, "Base type mismatch error"
    return True, a.baseType
