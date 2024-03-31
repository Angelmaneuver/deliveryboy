import os
import shutil
from pathlib import Path

from watchdog.events import FileSystemEvent

from deliveryboy.types import Data, Origin

from .abc import AbstractEventHandler


class TerminalEventHandler(AbstractEventHandler):
    def __init__(self, base: str, dest: str, queue: Data, entry: Data) -> None:
        self._base = Path(base)
        self._dest = Path(dest)
        self._queue = queue["data"]
        self._lock4queue = queue["lock"]
        self._entry = entry["data"]
        self._lock4entry = entry["lock"]

    def on_created(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return

        src = Path(event.src_path)
        id = src.stem
        extension = "".join(src.suffixes)

        index, entry = next(
            filter(lambda registered: registered[1]["id"] == id, enumerate(self._entry))
        )

        origin = entry["origin"]

        paths = self._dest
        if len(origin["paths"]) > 0:
            paths = self._dest.joinpath(origin["paths"])
            paths.mkdir(exist_ok=True, parents=True)

        basename = f"{origin['basename']}{extension}"

        dest = str(paths.joinpath(basename))

        with self._lock4entry:
            self._entry.pop(index)

            shutil.move(str(src), dest)

            if len(origin["paths"]) == 0:
                return

            path = self._base / Path(origin["paths"])

            if self.isRemain(origin, path):
                return

            path.rmdir()

            for i in range(1, origin["paths"].count(os.sep) + 1):
                if self.isRemain(origin, path.parents[i]):
                    return

                path.parents[i].rmdir()

    def isRemain(self, origin: Origin, path: Path) -> bool:
        entring = next(
            filter(
                lambda entry: not entry["origin"]["paths"].startswith(origin["paths"]),
                self._entry,
            ),
            None,
        )

        if entring is not None:
            return True

        exisiting = next(
            filter(lambda value: not str(value).startswith("."), list(path.iterdir())),
            None,
        )

        if exisiting is not None:
            return True

        with self._lock4queue:
            queueing = next(
                filter(
                    lambda queue: not queue["origin"]["paths"].startswith(
                        origin["paths"]
                    ),
                    self._queue,
                ),
                None,
            )

            if queueing is not None:
                return True

        return False
