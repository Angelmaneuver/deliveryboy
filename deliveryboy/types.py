from datetime import datetime
from threading import Lock
from typing import Tuple, TypedDict


class Origin(TypedDict):
    full: str
    paths: str
    basename: str
    extension: str


class Entry(TypedDict):
    id: str
    origin: Origin


class RequestQueue(TypedDict):
    data: dict[Tuple[datetime, Entry]]
    lock: Lock


class ResponseQueue(TypedDict):
    data: dict[Tuple[datetime, str]]
    lock: Lock


class QueueSet(TypedDict):
    request: RequestQueue
    response: ResponseQueue


class Data(TypedDict):
    data: list[Entry]
    lock: Lock
