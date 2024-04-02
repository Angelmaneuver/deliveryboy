from watchdog.events import FileSystemEvent

from deliveryboy.types import ResponseQueue

from .abc import AbstractEventHandler


class TerminalEventHandler(AbstractEventHandler):
    def __init__(self, base: str, queue: ResponseQueue) -> None:
        super().__init__(base)

        self._queue = queue["data"]
        self._lock = queue["lock"]

    def on_created(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return

        with self._lock:
            self._queue[event.src_path] = (self.now, event.src_path)

    def on_modified(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return

        with self._lock:
            self._queue[event.src_path] = (self.now, event.src_path)
