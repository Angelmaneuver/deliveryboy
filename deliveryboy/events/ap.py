import os
import shutil
from threading import Lock
from uuid import uuid4 as uuid

from watchdog.events import FileSystemEvent

from deliveryboy.types import Entry, Origin

from .abc import AbstractEventHandler


class APEventHandler(AbstractEventHandler):
    def on_created(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return

        id = str(uuid())
        src = event.src_path
        dirname = os.path.dirname(src)
        basename = os.path.splitext(os.path.basename(src))[0]
        _, extension = os.path.splitext(src)

        replace = self._base
        if dirname.startswith(f"{replace}{os.sep}"):
            replace += os.sep

        paths = dirname.replace(replace, "", 1)

        dest = os.path.join(self._dest, id)

        with self._lock:
            self._entry.append(
                Entry(
                    id=id,
                    origin=Origin(
                        full=src,
                        paths=paths,
                        basename=basename,
                        extension=extension,
                    ),
                )
            )

            shutil.move(src, dest)
