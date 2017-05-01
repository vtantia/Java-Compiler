class ThreeAddressCode(object):

    def __init__(self):
        self.code = []
        self.curTempCnt = 0
        self.data = []

    def emit(self, opCode, arg1=None, arg2=None, arg3=None):
        self.code += [[opCode, arg1, arg2, arg3]]

    def backpatch(self, bpList, jumpAddress):
        for lineNo in bpList:
            if not isinstance(lineNo, int):
                print('Wrong Entry {} passed to backpatch in backpatch List'.
                        format(lineNo))
            else:
                toPatch = self.code[lineNo]
                # Every Jump OpCode starts with letter 'J'
                if toPatch[0][0] is not 'J':
                    print('Wrong Entry to patch: {}'.format(toPatch))
                else:
                    # Assuming jump address is always at first position for
                    # jump instructions
                    toPatch[1] = jumpAddress

    def nextquad(self):
        return len(self.code)

    def allotNewTemp(self):
        self.curTempCnt += 1
        return 't' + str(self.curTempCnt)

    def addDataString(self, val):
        name = 'str' + str(len(self.data) + 1)
        self.data.append(name + ': .ascii\t' + val)
        return name

    def addDataInt(self, val):
        name = 'int' + str(len(self.data) + 1)
        self.data.append(name + ': .word\t' + val)
        return name
