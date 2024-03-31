import os
import threading

from . import watcher
from .events import APEventHandler, TerminalEventHandler
from .types import Data


def start(
    request: str, destination: str, pickuppoint: str, response: str, max_queue_size=50
) -> None:
    is_valid(request)
    is_valid(response)
    is_valid(destination)
    is_valid(pickuppoint)

    queue: Data = {"data": [], "lock": threading.Lock()}
    entry: Data = {"data": [], "lock": threading.Lock()}

    threads = {
        "ap": {
            "watch": threading.Thread(
                target=watcher.ap.regist,
                args=(
                    request,
                    APEventHandler(request, queue),
                ),
            ),
            "move": threading.Thread(
                target=watcher.ap.move,
                args=(
                    destination,
                    queue,
                    entry,
                    max_queue_size,
                ),
            ),
        },
        "terminal": threading.Thread(
            target=watcher.terminal.regist,
            args=(
                pickuppoint,
                TerminalEventHandler(request, response, queue, entry),
            ),
        ),
    }

    threads["ap"]["watch"].start()
    threads["ap"]["move"].start()
    threads["terminal"].start()

    threads["ap"]["watch"].join()
    threads["ap"]["move"].join()
    threads["terminal"].join()


def is_valid(path: str):
    if not os.path.isdir(path):
        raise NotADirectoryError(path)
