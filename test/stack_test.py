import unittest
from common import Stack


class StackTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__stack = Stack()
        self.__stack.push(1)
        self.__stack.push(2)
        self.__stack.push(3)
        self.__stack.push(4)
        self.__stack.push(5)

    def testPop(self) -> None:
        self.assertIn(5, self.__stack.pop())
        self.assertEqual(4, len(self.__stack))

    def testPush(self) -> None:
        self.__stack.push(6)
        self.assertIn(6, self.__stack.pop())
        self.assertEqual(5, len(self.__stack))

    def testFindKey(self) -> None:
        self.assertTrue(self.__stack.findKey(1))
        self.assertFalse(self.__stack.findKey(999999))

    def testPushEmptyKey(self) -> None:
        with self.assertRaises(Exception):
            self.__stack.push(None)

    def testPopAll(self) -> None:
        for _ in range(6):
            item = self.__stack.pop()
        self.assertTrue(not item)


def StackTestSuite() -> unittest.TestSuite:
    suite = unittest.TestSuite()
    suite.addTest(StackTest("testPop"))
    suite.addTest(StackTest("testPush"))
    suite.addTest(StackTest("testFindKey"))
    suite.addTest(StackTest("testPushEmptyKey"))
    suite.addTest(StackTest("testPopAll"))
    return suite
