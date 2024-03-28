from typing import TypedDict


class Origin(TypedDict):
    full: str
    paths: str
    basename: str
    extension: str


class Entry(TypedDict):
    id: str
    origin: Origin
