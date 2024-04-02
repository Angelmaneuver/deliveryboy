import shutil
import time
from datetime import datetime
from pathlib import Path

from watchdog.observers.polling import PollingObserver as Observer

from deliveryboy.types import Data, RequestQueue


def regist(path: str, event_handler: any, wait: int = 1):
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
    queue: RequestQueue,
    entry: Data,
    max_queue_size: int,
    wait: int = 1,
    threshold: int = 1,
):
    path = Path(dest)

    while True:
        if len(queue["data"]) == 0:
            time.sleep(wait)
            continue

        if len(entry["data"]) >= max_queue_size:
            time.sleep(wait)
            continue

        for key, value in queue["data"].items():
            lasttime, request = value

            if (datetime.now() - lasttime).total_seconds() > threshold:
                with queue["lock"]:
                    del queue["data"][key]

                try:
                    shutil.move(request["origin"]["full"], path.joinpath(request["id"]))

                    with entry["lock"]:
                        entry["data"].append(request)

                except FileNotFoundError:
                    pass

                break

        time.sleep(wait)
