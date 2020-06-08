from .linked_list import LinkedList

class Stack(LinkedList):
    def __init__(self):
        super().__init__()

    def push(self, key, data = None):
        if not key:
            raise Exception('Invaild input')
        self.pushHead(key, data)

    def pop(self):
        if len(self) == 0:
            return None
        node = self.popHead()
        return (node.key, node.data)
