import os
import shutil
from pathlib import Path

from watchdog.events import FileSystemEvent

from deliveryboy.types import Origin

from .abc import AbstractEventHandler


class TerminalEventHandler(AbstractEventHandler):
    def on_created(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return

        src = event.src_path
        id, extension = os.path.splitext(os.path.basename(src))

        index, entry = next(
            filter(lambda registered: registered[1]["id"] == id, enumerate(self._entry))
        )

        origin = entry["origin"]

        paths = self._dest
        if len(origin["paths"]) > 0:
            paths = os.path.join(self._dest, origin["paths"])
            os.makedirs(paths, exist_ok=True)

        basename = f"{origin['basename']}{extension}"

        dest = os.path.join(paths, basename)

        with self._lock:
            self._entry.pop(index)

            shutil.move(src, dest)

            if len(origin["paths"]) == 0:
                return

            path = Path(self._base) / Path(origin["paths"])

            if self.isRemain(path):
                return

            path.rmdir()

            for i in range(1, origin["paths"].count(os.sep) + 1):
                if self.isRemain(path.parents[i]):
                    return

                path.parents[i].rmdir()

    def isRemain(self, origin: Origin, path: Path) -> bool:
        entring = next(
            filter(
                lambda entry: not entry["origin"]["paths"].startWith(origin["paths"]),
                self._entry,
            ),
            None,
        )

        if entring is not None:
            return True

        exisiting = next(
            filter(lambda value: not value.startWith("."), list(path.iterdir())),
            None,
        )

        if exisiting is not None:
            return True

        else:
            return False
