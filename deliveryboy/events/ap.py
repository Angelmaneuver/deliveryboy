from watchdog.events import FileSystemEvent

from deliveryboy.types import RequestQueue

from .abc import AbstractEventHandler


class APEventHandler(AbstractEventHandler):
    def __init__(self, base: str, queue: RequestQueue) -> None:
        super().__init__(base)

        self._queue = queue["data"]
        self._lock = queue["lock"]

    def on_created(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return

        with self._lock:
            self._queue[event.src_path] = (
                self.now,
                self.get_entry(self._base, event.src_path),
            )

    def on_modified(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return

        with self._lock:
            entry = None

            if event.src_path in self._queue:
                _, entry = self._queue[event.src_path]
            else:
                entry = self.get_entry(self._base, event.src_path)

            self._queue[event.src_path] = (self.now, entry)
