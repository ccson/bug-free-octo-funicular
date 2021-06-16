import os
import requests
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Watcher(object):

    WATCH_DIRECTORY = "/uploads"
    SLEEP_INTERVAL = 10

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, Watcher.WATCH_DIRECTORY, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(Watcher.SLEEP_INTERVAL)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if not event.is_directory and event.event_type == 'created':
            imdb_id, file_extension = os.path.splitext(event.src_path)
            file_extension = file_extension.lstrip('.')
            data = {'imdb_id': imdb_id, 'file_extension': file_extension}
            post_response = requests.post(
                url='http://backend:80/transcode',
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            post_response.raise_for_status()


if __name__ == '__main__':
    watch = Watcher()
    watch.run()
