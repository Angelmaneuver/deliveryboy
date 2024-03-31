from threading import Lock
from typing import TypedDict


class Origin(TypedDict):
    full: str
    paths: str
    basename: str
    extension: str


class Entry(TypedDict):
    id: str
    origin: Origin


class Data(TypedDict):
    data: list[Entry]
    lock: Lock
