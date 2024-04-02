from watchdog.events import FileSystemEventHandler

from deliveryboy.common import get_entry, get_now


class AbstractEventHandler(FileSystemEventHandler):
    def __init__(self, base: str) -> None:
        super().__init__()

        self._base = base

    @property
    def now(self):
        return get_now()

    def get_entry(self, base, path):
        return get_entry(base, path)
