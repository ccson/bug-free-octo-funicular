from . import db

import json


class Movie(db.Model):
    '''
    Table that stores the movie attributes fetched from the TMDB database
    '''

    __tablename__ = 'movie'

    imdb_id = db.Column(db.String(24), primary_key=True)
    tmdb_id = db.Column(db.String(24))
    title_name = db.Column(db.String(256))
    release_year = db.Column(db.SmallInteger())
    film_rating = db.Column(db.String(12))
    runtime = db.Column(db.SmallInteger())
    genres = db.Column(db.String(256))
    poster_artwork = db.Column(db.String(256))
    rating = db.Column(db.Numeric())

    def __init__(self, imdb_id, tmdb_id, title_name, release_year, film_rating, runtime, genres, poster_artwork, rating):
        self.imdb_id = imdb_id
        self.tmdb_id = tmdb_id
        self.title_name = title_name
        self.release_year = release_year
        self.film_rating = film_rating
        self.runtime = runtime
        self.genres = genres
        self.poster_artwork = poster_artwork
        self.rating = rating

    def __repr__(self):
        return json.dumps({
            'imdb_id': self.imdb_id,
            'tmdb_id': self.tmdb_id,
            'title_name': self.title_name,
            'release_year': self.release_year,
            'film_rating': self.film_rating,
            'runtime': self.runtime,
            'genres': self.genres,
            'poster_artwork': self.poster_artwork,
            'rating': str(self.rating),
        })


class TranscodingMetadata(db.Model):
    '''
    Table that stores all the metadata related to the video transcoding process
    '''

    __tablename__ = 'transcoding_metadata'

    imdb_id = db.Column(db.String(24), primary_key=True)
    done_transcoding = db.Column(db.Boolean(), default=False)
    transcode_timestamp = db.Column(db.DateTime())
    transcode_file_size = db.Column(db.BigInteger())
    original_file_size = db.Column(db.BigInteger())

    def __init__(self, imdb_id, done_transcoding):
        self.imdb_id = imdb_id
        self.done_transcoding = done_transcoding

    def set_done_transcoding(self, done_transcoding):
        self.done_transcoding = done_transcoding

    def set_transcode_timestamp(self, transcode_timestamp):
        self.transcode_timestamp = transcode_timestamp

    def set_transcode_file_size(self, transcode_file_size):
        self.transcode_file_size = transcode_file_size

    def set_original_file_size(self, original_file_size):
        self.original_file_size = original_file_size

    def __repr__(self):
        return json.dumps({
            'imdb_id': self.imdb_id,
            'done_transcoding': self.done_transcoding,
            'transcode_timestamp': self.transcode_timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f'),
            'transcode_file_size': self.transcode_file_size,
            'original_file_size': self.original_file_size
        })
