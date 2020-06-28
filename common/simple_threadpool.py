from threading import Lock
import multiprocessing
from multiprocessing import Pool
from typing import (
    Tuple,
    Optional,
    TypeVar,
    List,
    Any,
    Callable,
)

multiprocessing.set_start_method('fork')

def handler(index: int) -> Tuple[int, Optional[Any]]:
    pass

class ThreadPool():
    def __init__(self, tasks: List[Callable[[], Optional[Any]]], nthreads: int) -> None:
        if tasks is None or len(tasks) <= 0:
            raise Exception("No task found")
        super().__init__()
        self.__taskList: List[Callable[[], Optional[Any]]] = tasks
        self.__nthreads: int = min(nthreads, len(tasks))
        self.__result: List[Optional[Any]] = [None for _ in range(len(self.__taskList))]
        self.__poolLock: Lock = Lock()

    @property
    def result(self):
        try:
            self.__poolLock.acquire()
            return self.__result
        finally:
            self.__poolLock.release()

    def startAndWait(self):
        try:
            self.__poolLock.acquire()

            global handler
            def handler(index: int) -> Tuple[int, Optional[Any]]:
                return index, self.__taskList[index]()

            with Pool(processes = self.__nthreads) as pool:
                for i, res in pool.map(handler, range(len(self.__taskList))):
                    self.__result[i] = res
        finally:
            self.__poolLock.release()
