import time

from watchdog.observers import Observer


def regist(path: str, event_handler: any, wait=1):
    observer = Observer()

    observer.schedule(event_handler, path, recursive=True)

    observer.start()

    try:
        while True:
            time.sleep(wait)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()
