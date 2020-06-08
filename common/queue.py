from .linked_list import LinkedList

class Queue(LinkedList):
    def __init__(self):
        super().__init__()

    def enqueue(self, key, data = None):
        if not key:
            raise Exception("Key is None")
        self.pushHead(key, data)

    def dequeue(self):
        if len(self) == 0:
            return None
        node = self.popTail()
        return (node.key, node.data)
