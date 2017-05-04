class Temp(object):
    def __init__(self, num, lastTable):
        self.tempNum = num
        lastTable['size'] += 4
        self.offset = lastTable['size']
