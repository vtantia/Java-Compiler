class ThreeAddressCode(object):

    def __init__(self):
        self.code = []
        self.curTempCnt = 0
        self.data = []
        self.labelMap = {}

    def emit(self, opCode, arg1=None, arg2=None, arg3=None):
        self.code += [[opCode, arg1, arg2, arg3]]

    def backpatch(self, bpList, jumpAddress, label=None):
        label = self.getLabel(label, jumpAddress)

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
                    toPatch[1] = label

    def getLabel(self, label, jumpAddress):
        if self.labelMap.get(label):
            if self.labelMap[label] != jumpAddress:
                label = None

        if not label:
            label = 'label' + str(len(self.labelMap))
        self.labelMap[label] = jumpAddress
        return label

    def getLabelFunc(self, label):
        assert label
        i = 1
        while self.labelMap.get(label + str(i)):
            i += 1

        self.labelMap[label + str(i)] = self.nextquad()
        return label + str(i)

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

    def returnFunc(self, sizeParams):
        self.emit('mov', '$sp', '$30')
        self.emit('lw', '$30', '($sp)')
        self.emit('lw', '$31', '4($sp)')
        self.emit('addi', '$sp', '$sp', 8)
        self.emit('addi', '$sp', '$sp', sizeParams)
        self.emit('JR', '$31')

    def pushParams(self, tempList):
        if tempList:
            self.emit('subi', '$sp', '$sp', 4*len(tempList))

        for i in range(0, len(tempList)):
            self.emit('sw', tempList[i], str(4*i) + '($sp)')

    def getDynamicMem(self, size):
        self.emit('li', '$v0', 9)
        self.emit('li', '$a0', size)
        self.emit('syscall')

    # Used for constructor
    def commonInvocation(self, pObj, pArg, func):
        if pArg:
            self.tac.pushParams([pObj.temporary] + pArg.tempList)
        else:
            self.tac.pushParams([pObj.temporary])

        self.tac.emit('jal', func['funcLabel'])
        self.tac.emit('nop')

    def methodInvocation(self, pObj, pArg, func):
        self.commonInvocation(pObj, pArg, func)
        self.emit('mov', pObj.temporary, '$v0')
