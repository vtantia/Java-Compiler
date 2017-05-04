from Temp import Temp

class ThreeAddressCode(object):

    def __init__(self):
        self.code = []
        self.data = []
        self.labelMap = {}

    def emit(self, opCode, *arg):#arg1=None, arg2=None, arg3=None):
        arr2 = ['fake' + opCode]
        arr = [opCode]
        isCalc = opCode in ['subi', 'lw', 'move', 'addi', 'mflo', 'mfhi', 'add', 'la', 'li', 'sub', 'sllv', 'srlv', 'and', 'or', 'xor', 'nor']

        addFake = False

        for i, item in enumerate(arg):
            if not isinstance(item, Temp):
                arr.append(item)
                arr2.append(item)
            else:
                regStr = '$t' + str(i)
                if not isCalc or i != 0:
                    self.emit('lw', regStr, str(-item.offset) + '($30)')
                arr.append(regStr)
                arr2.append('temp' + str(item.tempNum))
                addFake = True

        while len(arr) < 4:
            arr.append(None)

        self.code.append(arr)
        # self.code += [[opCode, arg1, arg2, arg3]]

        if isCalc and isinstance(arg[0], Temp):
            self.emit('sw', '$t0', str(-arg[0].offset) + '($30)')

        # if addFake:
            # self.code.append(arr2)

    def backpatch(self, bpList, jumpAddress, label=None): #Why label None
        label = self.getLabel(label, jumpAddress)

        for lineNo in bpList:
            if not isinstance(lineNo, int):
                print('Wrong Entry {} passed to backpatch in backpatch List'.
                        format(lineNo))
            else:
                toPatch = self.code[lineNo]
                for i in range(len(toPatch)):
                    if type(toPatch[i]) == 'str':
                        toPatch[i] = toPatch[i].replace('...', 'label')

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
        i = 0
        while self.labelMap.get(label + str(i)):
            i += 1

        self.labelMap[label + str(i)] = self.nextquad()
        return label + str(i)

    def nextquad(self):
        return len(self.code)

    def addDataString(self, val):
        name = 'str' + str(len(self.data) + 1)
        self.data.append(name + ': .ascii\t' + val)
        return name

    def addDataInt(self, val):
        name = 'int' + str(len(self.data) + 1)
        self.data.append(name + ': .word\t' + val)
        return name

    def returnFunc(self, sizeParams):
        self.emit('move', '$sp', '$30')
        self.emit('lw', '$30', '($sp)')
        self.emit('lw', '$31', '4($sp)')
        self.emit('addi', '$sp', '$sp', 8)
        self.emit('addi', '$sp', '$sp', sizeParams)
        self.emit('jr', '$31')

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
            self.pushParams([pObj.temporary] + pArg.tempList)
        else:
            self.pushParams([pObj.temporary])

        self.emit('jal', func['funcLabel'])
        self.emit('nop')

    def methodInvocation(self, pObj, pArg, func):
        self.commonInvocation(pObj, pArg, func)
        self.emit('move', pObj.temporary, '$v0')
