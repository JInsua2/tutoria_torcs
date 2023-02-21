class CircularQueue(object):

    def __init__(self, elem):
        self.cola = []
        self.cola.append(elem)
        self.front = 1

    def añadir(self, other):
        if len(self.cola) < 2:
            self.cola.append(other)
        else:
            self.cola[self.front] = other
        self.front = (self.front + 1) % 2

    def getCola(self):
        return self.cola
