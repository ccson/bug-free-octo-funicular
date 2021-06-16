import json

from flask import Flask
from flask import request

from .init import create_app
from .model import db, Movie, TranscodingMetadata

from .services.video_transcoder import VideoTranscoder
from .services.tmdb_service import TmdbService

app = create_app()


@app.route('/health_check')
def health_check():
    db.engine.execute('SELECT 1')
    return '', 200


@app.route('/', methods=['GET'])
def get_movie_details():
    # return 'Hello World!'
    return Movie.query \
        .join(TranscodingMetadata, Movie.tmdb_id == TranscodingMetadata.tmdb_id) \
        .add_columns(Movie.title_name) \
        .all()


@app.route('/movie_details', methods=['GET'])
def test():
    tmdb_id = request.args.get('tmdb_id')
    return TmdbService.get_movie_details(tmdb_id)


@app.route('/transcode', methods=['POST'])
def transcode_video():
    json_response = json.loads(request.get_data())
    imdb_id = json_response['imdb_id']
    file_extension = json_response['file_extension']
    return VideoTranscoder.run(imdb_id, file_extension)


if __name__ == '__main__':
    app.run()
