import unittest
from common import Queue


class QueueTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__queue = Queue()
        self.__queue.enqueue(1)
        self.__queue.enqueue(2)
        self.__queue.enqueue(3)
        self.__queue.enqueue(4)
        self.__queue.enqueue(5)

    def testDequeue(self) -> None:
        self.assertIn(1, self.__queue.dequeue())
        self.assertEqual(4, len(self.__queue))

    def testEnqueue(self) -> None:
        self.__queue.enqueue(6)
        self.assertIn(1, self.__queue.dequeue())
        self.assertEqual(5, len(self.__queue))

    def testFindKey(self) -> None:
        self.assertTrue(self.__queue.findKey(1))
        self.assertFalse(self.__queue.findKey(999999))

    def testEnqueueEmptyKey(self) -> None:
        with self.assertRaises(Exception):
            self.__queue.enqueue(None)

    def testDequeueAll(self) -> None:
        for _ in range(6):
            item = self.__queue.dequeue()
        self.assertTrue(not item)


def QueueTestSuite() -> unittest.TestSuite:
    suite = unittest.TestSuite()
    suite.addTest(QueueTest("testDequeue"))
    suite.addTest(QueueTest("testEnqueue"))
    suite.addTest(QueueTest("testFindKey"))
    suite.addTest(QueueTest("testEnqueueEmptyKey"))
    suite.addTest(QueueTest("testDequeueAll"))
    return suite
