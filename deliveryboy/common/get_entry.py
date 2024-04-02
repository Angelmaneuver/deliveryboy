import os
from pathlib import Path
from uuid import uuid4 as uuid

from deliveryboy.types import Entry, Origin


def get_entry(_base: str, _path: str) -> Entry:
    id = str(uuid())

    path = Path(_path)
    dirname = str(path.parent)
    basename = path.stem
    extension = "".join(path.suffixes)

    replace = _base
    if dirname.startswith(f"{replace}{os.sep}"):
        replace += os.sep

    paths = dirname.replace(replace, "", 1)

    return Entry(
        id=id,
        origin=Origin(
            full=str(path),
            paths=paths,
            basename=basename,
            extension=extension,
        ),
    )
