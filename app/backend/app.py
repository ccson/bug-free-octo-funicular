import json

from flask import request

from . import app, db
from .model import Movie, TranscodingMetadata

from .services.video_transcoder import VideoTranscoder
from .services.tmdb_service import TmdbService

with app.app_context():
    db.create_all()
    db.session.commit()


@app.route('/health_check')
def health_check():
    db.engine.execute('SELECT 1')
    return '', 200


@app.route('/', methods=['GET'])
def get_movie_details():
    return str(Movie.query \
        .join(TranscodingMetadata, Movie.imdb_id == TranscodingMetadata.imdb_id) \
        .add_columns(Movie.title_name) \
        .all())


@app.route('/transcode', methods=['POST'])
def transcode_video():
    json_response = json.loads(request.get_data())
    imdb_id = json_response['imdb_id']
    file_extension = json_response['file_extension']

    transcoding_metadata = TranscodingMetadata(imdb_id=imdb_id, done_transcoding=False)
    db.session.merge(transcoding_metadata)
    db.session.commit()

    video_transcoder = VideoTranscoder(imdb_id, file_extension)
    video_transcoder.run()

    transcoding_metadata.set_done_transcoding(True)
    transcoding_metadata.set_transcode_timestamp(video_transcoder.get_transcode_timestamp())
    transcoding_metadata.set_transcode_file_size(video_transcoder.get_output_file_size())
    transcoding_metadata.set_original_file_size(video_transcoder.get_input_file_size())
    db.session.merge(transcoding_metadata)
    db.session.commit()

    movie_data = TmdbService.get_movie_details(imdb_id)
    movie = Movie(**movie_data)
    db.session.merge(movie)
    db.session.commit()

    return '', 200


if __name__ == '__main__':
    app.run()
