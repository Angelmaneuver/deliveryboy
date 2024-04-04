from pathlib import Path


def is_ignore(_path: str) -> bool:
    path = Path(_path)
    dirname = str(path.parent)
    basename = path.stem
    extension = "".join(path.suffixes)

    if basename.startswith("."):
        return True

    return False
