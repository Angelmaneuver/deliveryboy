import os
import threading

from . import watcher
from .events import APEventHandler, TerminalEventHandler
from .types import Data, QueueSet


def start(
    request: str, destination: str, pickuppoint: str, response: str, max_queue_size=50
) -> None:
    is_valid(request)
    is_valid(response)
    is_valid(destination)
    is_valid(pickuppoint)

    queue: QueueSet = {
        "request": {"data": {}, "lock": threading.Lock()},
        "response": {"data": {}, "lock": threading.Lock()},
    }

    entry: Data = {"data": [], "lock": threading.Lock()}

    threads = {
        "ap": {
            "watch": threading.Thread(
                target=watcher.ap.regist,
                args=(
                    request,
                    APEventHandler(request, queue["request"]),
                ),
            ),
            "move": threading.Thread(
                target=watcher.ap.move,
                args=(
                    destination,
                    queue["request"],
                    entry,
                    max_queue_size,
                ),
            ),
        },
        "terminal": {
            "watch": threading.Thread(
                target=watcher.terminal.regist,
                args=(
                    pickuppoint,
                    TerminalEventHandler(response, queue["response"]),
                ),
            ),
            "move": threading.Thread(
                target=watcher.terminal.move,
                args=(
                    request,
                    queue["request"],
                    response,
                    queue["response"],
                    entry,
                ),
            ),
        },
    }

    threads["ap"]["watch"].start()
    threads["ap"]["move"].start()
    threads["terminal"]["watch"].start()
    threads["terminal"]["move"].start()

    threads["ap"]["watch"].join()
    threads["ap"]["move"].join()
    threads["terminal"]["watch"].join()
    threads["terminal"]["move"].join()


def is_valid(path: str):
    if not os.path.isdir(path):
        raise NotADirectoryError(path)
