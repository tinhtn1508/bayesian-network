import json
from typing import (
    Dict,
    Optional,
    Generic,
    Generator,
    TypeVar,
    List,
    Set,
    Tuple,
    Hashable,
    Any,
    Union,
)


class Parser:
    def __init__(self):
        pass

    def fromJson(self):
        raise NotImplementedError

    def fromTxt(self):
        pass
