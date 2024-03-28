from threading import Lock

from watchdog.events import FileSystemEventHandler

from deliveryboy.types import Entry


class AbstractEventHandler(FileSystemEventHandler):
    def __init__(self, base: str, dest: str, entry: list[Entry], lock: Lock) -> None:
        super().__init__()

        self._base = base
        self._dest = dest
        self._entry = entry
        self._lock = lock
