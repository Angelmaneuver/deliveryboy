import os
import shutil
import time
from datetime import datetime
from pathlib import Path

from watchdog.observers import Observer

from deliveryboy.types import Data, Entry, Origin, RequestQueue, ResponseQueue


def regist(path: str, event_handler: any, wait: int = None):
    observer = Observer()

    observer.schedule(event_handler, path, recursive=True)

    observer.start()

    try:
        while True:
            if wait is not None:
                time.sleep(wait)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()


def move(
    dest: str,
    request_queue: RequestQueue,
    response_queue: ResponseQueue,
    entry: Data,
    wait: int = 1,
    threshold: int = 1,
):
    base = Path(dest)

    while True:
        if len(response_queue["data"]) == 0:
            time.sleep(wait)
            continue

        for key, value in response_queue["data"].items():
            lasttime, response = value

            if (datetime.now() - lasttime).total_seconds() > threshold:
                with response_queue["lock"]:
                    del response_queue["data"][key]

                transfer(Path(response), base, request_queue, entry)

                break

        time.sleep(wait)


def transfer(
    src: Path,
    base: Path,
    queue: RequestQueue,
    entry: Data,
):
    id = src.stem
    extension = "".join(src.suffixes)

    index, entry_data = next(
        filter(
            lambda registered: registered[1]["id"] == id,
            enumerate(entry["data"]),
        )
    )

    origin = entry_data["origin"]

    paths = base
    if len(origin["paths"]) > 0:
        paths = base.joinpath(origin["paths"])
        paths.mkdir(exist_ok=True, parents=True)

    basename = f"{origin['basename']}{extension}"

    dest = str(paths.joinpath(basename))

    with entry["lock"]:
        entry["data"].pop(index)

    shutil.move(str(src), dest)

    if len(origin["paths"]) == 0:
        return

    path = base / Path(origin["paths"])

    if isRemain(queue, entry, origin, path):
        return

    path.rmdir()

    for i in range(1, origin["paths"].count(os.sep) + 1):
        if isRemain(queue, entry, origin, path.parents[i]):
            return

        path.parents[i].rmdir()


def isRemain(queue: RequestQueue, entry: Entry, origin: Origin, path: Path) -> bool:
    entring = next(
        filter(
            lambda entry: not entry["origin"]["paths"].startswith(origin["paths"]),
            entry,
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

    queueing = next(
        filter(
            lambda queue: not queue["origin"]["paths"].startswith(origin["paths"]),
            queue["data"],
        ),
        None,
    )

    if queueing is not None:
        return True

    return False
