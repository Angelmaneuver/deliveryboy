import os
from pathlib import Path
from uuid import uuid4 as uuid

from watchdog.events import FileSystemEvent

from deliveryboy.types import Entry, Origin, RequestQueue

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
            self._queue[event.src_path] = (self.now, self.get_entry(event.src_path))

    def on_modified(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return

        with self._lock:
            entry = None

            if event.src_path in self._queue:
                _, entry = self._queue[event.src_path]
            else:
                entry = self.get_entry(event.src_path)

            self._queue[event.src_path] = (self.now, entry)

    def get_entry(self, path: str) -> Entry:
        id = str(uuid())
        src = Path(path)
        dirname = str(src.parent)
        basename = src.stem
        extension = "".join(src.suffixes)

        replace = self._base
        if dirname.startswith(f"{replace}{os.sep}"):
            replace += os.sep

        paths = dirname.replace(replace, "", 1)

        return Entry(
            id=id,
            origin=Origin(
                full=str(src),
                paths=paths,
                basename=basename,
                extension=extension,
            ),
        )
