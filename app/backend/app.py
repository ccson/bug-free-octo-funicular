from flask import Flask
from flask import request

from .model import TranscodingMetadata, TmdbMetadata

from .tmdb_service import TmdbService
from .video_transcoder import VideoTranscoder


app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    return "Hello World!"


@app.route('/movie_details', methods=['GET'])
def get_movie_details():
    tmdb_id = request.args.get('tmdb_id')
    return TmdbService.get_movie_details(tmdb_id)


@app.route('/transcode', methods=['POST'])
def transcode_video(name):
    return "Hello {}!".format(name)


if __name__ == '__main__':
    app.run()
