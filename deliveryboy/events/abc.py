from watchdog.events import FileSystemEventHandler


class AbstractEventHandler(FileSystemEventHandler):
    def __init__(self, base: str) -> None:
        super().__init__()

        self._base = base
