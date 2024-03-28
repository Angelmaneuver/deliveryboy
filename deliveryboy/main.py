import os
import threading

from . import watcher
from .events import APEventHandler, TerminalEventHandler
from .types import Entry


def start(request: str, destination: str, pickuppoint: str, response: str) -> None:
    is_valid(request)
    is_valid(response)
    is_valid(destination)
    is_valid(pickuppoint)

    entry: list[Entry] = []
    lock = threading.Lock()

    threads = {
        "ap": threading.Thread(
            target=watcher.ap.regist,
            args=(
                request,
                APEventHandler(request, destination, entry, lock),
            ),
        ),
        "terminal": threading.Thread(
            target=watcher.terminal.regist,
            args=(
                pickuppoint,
                TerminalEventHandler(request, response, entry, lock),
            ),
        ),
    }

    threads["ap"].start()
    threads["terminal"].start()

    threads["ap"].join()
    threads["terminal"].join()


def is_valid(path: str):
    if not os.path.isdir(path):
        raise NotADirectoryError(path)
