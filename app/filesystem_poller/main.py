import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Watcher(object):
    watchDirectory = "/give / the / address / of / directory"

    SLEEP_INTERVAL = 10

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive=False)
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
            # Event is created, you can process it now
            print("Watchdog received created event - % s." % event.src_path)


if __name__ == '__main__':
    watch = Watcher()
    watch.run()
