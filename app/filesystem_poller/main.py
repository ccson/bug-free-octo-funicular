import logging
import os
import requests
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, EVENT_TYPE_CREATED, EVENT_TYPE_MODIFIED

LOGGER = logging.getLogger('FILESYSTEM_POLLER')
LOGGER.setLevel('INFO')


class Watcher(object):
    '''
    The Filesystem watcher/poller that will trigger an event handler when an event occurs on the
    video uploads folder.
    '''

    WATCH_DIRECTORY = os.getenv('UPLOADS_FOLDER')
    SLEEP_INTERVAL = 10

    def __init__(self):
        self.observer = Observer()

    def run(self):
        '''
        Instantiates the event handler and runs the observer. It will set the observer to use the event handler
        whenever the observer/watcher catches an event.
        '''
        event_handler = Handler()
        self.observer.schedule(event_handler, Watcher.WATCH_DIRECTORY, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(Watcher.SLEEP_INTERVAL)
        except:
            self.observer.stop()
            LOGGER.error('Observer Stopped')

        self.observer.join()


class Handler(FileSystemEventHandler):
    '''
    The event handler that the observer/watcher will run when it detects a file system event.
    '''

    @staticmethod
    def on_any_event(event):
        '''
        Overwrites the parent class's method to trigger the downstream tasks of transcoding the video and
        fetching the movie details from the TMDB ID.
        '''
        try:
            # The EVENT_TYPE_MODIFIED is used to account for when a file is copied, since a copy doesn't trigger
            # an EVENT_TYPE_CREATED instead.
            if not event.is_directory and event.event_type in (EVENT_TYPE_CREATED, EVENT_TYPE_MODIFIED):
                file_name, file_extension = os.path.splitext(event.src_path)
                imdb_id = os.path.basename(file_name)
                file_extension = file_extension.lstrip('.')
                data = {'imdb_id': imdb_id, 'file_extension': file_extension}
                post_response = requests.post(
                    url='http://backend:80/transcode',
                    json=data,
                    headers={'Content-Type': 'application/json'}
                )
                post_response.raise_for_status()
        except:
            LOGGER.error(f'Event Completed Unsuccessfuly For File ({event.src_path})')


if __name__ == '__main__':
    watch = Watcher()
    watch.run()
