import os
from pathlib import Path
from uuid import uuid4 as uuid

from watchdog.events import FileSystemEvent

from deliveryboy.types import Data, Entry, Origin

from .abc import AbstractEventHandler


class APEventHandler(AbstractEventHandler):
    def __init__(self, base: str, queue: Data) -> None:
        super().__init__(base)

        self._queue = queue["data"]
        self._lock = queue["lock"]

    def on_created(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return

        id = str(uuid())
        src = Path(event.src_path)
        dirname = str(src.parent)
        basename = src.stem
        extension = "".join(src.suffixes)

        replace = self._base
        if dirname.startswith(f"{replace}{os.sep}"):
            replace += os.sep

        paths = dirname.replace(replace, "", 1)

        with self._lock:
            self._queue.append(
                Entry(
                    id=id,
                    origin=Origin(
                        full=str(src),
                        paths=paths,
                        basename=basename,
                        extension=extension,
                    ),
                )
            )
