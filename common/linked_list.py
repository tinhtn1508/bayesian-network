from typing import Any, TypeVar, Generator

class LLNode(object):
    def __init__(self, key: Any, data: Any = None):
        self.key = key
        self.data = data
        self.prev: LLNode = None
        self.next: LLNode = None

    def __lt__(self, b) -> bool:
        return self.key < b.key

    def __gt__(self, b) -> bool:
        return self.key > b.key

    def __str__(self) -> bool:
        return str(self.key)

class LinkedList(object):
    def __init__(self):
        self.head: LLNode = None
        self.tail: LLNode = None
        self.length: int = 0

    def __len__(self) -> int:
        return self.length

    def __str__(self) -> str:
        result = "# "
        for node in self.iterateForward():
            result += (str(node.key) + " <-> ")
        result += '#\n'
        result += f"checkInvariant: {self.checkInvariant()}\n"
        return result

    def pushHeadBatch(self, keys: Any, data: Any = []) -> None:
        for i in range(len(keys)):
            if i >= len(data):
                self.pushHead(keys[i])
            else:
                self.pushHead(keys[i], data[i])

    def pushTailBatch(self, keys: Any, data: Any = []) -> None:
        for i in range(len(keys)):
            if i >= len(data):
                self.pushTail(keys[i])
            else:
                self.pushTail(keys[i], data[i])

    def pushHead(self, key: Any, data: Any = None) -> None:
        newNode: LLNode = LLNode(key, data)
        self.length += 1
        if not self.head:
            self.head = newNode
            self.tail = newNode
        else:
            newNode.next = self.head
            self.head.prev = newNode
            self.head = newNode

    def pushTail(self, key: Any, data: Any = None):
        newNode: LLNode = LLNode(key, data)
        self.length += 1
        if not self.tail:
            self.head = newNode
            self.tail = newNode
        else:
            newNode.prev = self.tail
            self.tail.next = newNode
            self.tail = newNode

    def popHead(self) -> LLNode:
        if not self.head:
            return None
        self.length -= 1
        nextNode: LLNode = self.head.next
        headNode: LLNode = self.head
        if not nextNode:
            self.tail = None
            self.head = None
            if self.length != 0:
                print(f"Warning: something wrong, linked list empty but length = {self.length}")
                self.length = 0
        else:
            self.head = nextNode
            nextNode.prev = None
        headNode.next = None
        return headNode

    def popTail(self) -> LLNode:
        if not self.tail:
            return None
        self.length -= 1
        prevNode: LLNode = self.tail.prev
        tailNode: LLNode = self.tail
        if not prevNode:
            self.tail = None
            self.head = None
            if self.length != 0:
                print(f"Warning: something wrong, linked list empty but length = {self.length}")
                self.length = 0
        else:
            self.tail = prevNode
            prevNode.next = None
        tailNode.prev = None
        return tailNode

    def iterateForward(self) -> Generator[LLNode, None, None]:
        node: LLNode = self.head
        while node:
            yield node
            node = node.next

    def iterateBackward(self) -> Generator[LLNode, None, None]:
        node = self.tail
        while node:
            yield node
            node = node.prev

    def findKey(self, key: Any, fwd: bool = True) -> LLNode:
        if fwd:
            for node in self.iterateForward():
                if node.key == key: return node
        else:
            for node in self.iterateBackward():
                if node.key == key: return node
        return None

    def insertAfter(self, node: LLNode, key: Any, data: Any = None) -> None:
        if not node:
            raise Exception("None node input")
        if node is self.tail:
            self.pushTail(key, data)
            return
        self.length += 1
        newNode = LLNode(key, data)
        nextNode = node.next
        newNode.prev = node
        newNode.next = nextNode
        node.next = newNode
        nextNode.prev = newNode

    def insertBefore(self, node: LLNode, key: Any, data: Any = None) -> None:
        if not node:
            raise Exception("None node input")
        if node is self.head:
            self.pushHead(key, data)
            return
        self.length += 1
        newNode = LLNode(key, data)
        prevNode = node.prev
        newNode.prev = prevNode
        newNode.next = node
        node.prev = newNode
        prevNode.next = newNode

    def increasementPush(self, key: Any, data: Any = None) -> None:
        if not self.head:
            self.pushHead(key, data)
            return
        for node in self.iterateBackward():
            if key > node.key:
                self.insertAfter(node, key, data)
                return
        self.pushHead(key, data)

    def decreasementPush(self, key: Any, data: Any = None):
        if not self.head:
            self.pushHead(key, data)
            return
        for node in self.iterateForward():
            if key > node.key:
                self.insertBefore(node, key, data)
                return
        self.pushTail(key, data)

    def removeNode(self, node: LLNode) -> LLNode:
        if not node:
            raise Exception("input node is None")
        if node is self.head:
            return self.popHead()
        elif node is self.tail:
            return self.popTail()
        else:
            prevNode = node.prev
            nextNode = node.next
            prevNode.next = nextNode
            nextNode.prev = prevNode
            self.length -= 1
        node.prev = None
        node.next = None
        return node

    def removeNthNode(self, nth: int) -> LLNode:
        node = None
        if nth >= self.length:
            raise Exception("input out of range")
        if nth == 0:
            return self.popHead()
        elif nth == (self.length - 1):
            return self.popTail()
        else:
            for i, n in enumerate(self.iterateForward()):
                if i == nth:
                    node = n
                    break
            prevNode = node.prev
            nextNode = node.next
            prevNode.next = nextNode
            nextNode.prev = prevNode
            self.length -= 1
        node.prev = None
        node.next = None
        return node

    def removeAll(self):
        self.head = None
        self.tail = None
        self.length = 0

    def checkInvariant(self):
        if not self.head and not self.tai and self.length == 0:
            return True
        if (not self.head and self.tail) or (self.head and not self.tail):
            return False
        n = 0
        for i, _ in enumerate(self.iterateForward()):
            n = i
        if (n + 1) == self.length:
            return True
        return False
