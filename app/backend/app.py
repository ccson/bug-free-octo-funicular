from flask import Flask
from flask import request

from .init import create_app
from .model import Movie, TranscodingMetadata

from .services.tmdb_service import TmdbService

app = create_app()


@app.route('/', methods=['GET'])
def index():
    return 'Hello World!'


@app.route('/movie_details', methods=['GET'])
def get_movie_details():
    tmdb_id = request.args.get('tmdb_id')
    return TmdbService.get_movie_details(tmdb_id)


@app.route('/transcode', methods=['POST'])
def transcode_video(name):
    return "Hello {}!".format(name)


if __name__ == '__main__':
    app.run()
