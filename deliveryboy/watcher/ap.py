import pathlib
import shutil
import time

from watchdog.observers.polling import PollingObserver as Observer

from deliveryboy.types import Data


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
    queue: Data,
    entry: Data,
    max_queue_size: int,
    wait=1,
):
    path = pathlib.Path(dest)

    while True:
        if len(queue["data"]) == 0:
            time.sleep(wait)
            continue

        if len(entry["data"]) >= max_queue_size:
            time.sleep(wait)
            continue

        with queue["lock"]:
            with entry["lock"]:
                request = queue["data"].pop()

                entry["data"].append(request)

                shutil.move(request["origin"]["full"], path.joinpath(request["id"]))

        time.sleep(wait)
