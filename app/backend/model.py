import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


class Movie(db.Model):
    __tablename__ = 'movie'

    tmdb_id = db.Column(db.Integer, primary_key=True)
    title_name = db.Column(db.String(256))
    release_year = db.Column(db.Date())
    film_rating = db.Column(db.String(12))
    runtime = db.Column(db.SmallInteger())
    genres = db.Column(db.String(256))
    poster_artwork = db.Column(db.String(256))
    rating = db.Column(db.Numeric())


class TranscodingMetadata(db.Model):
    __tablename__ = 'transcoding_metadata'

    tmdb_id = db.Column(db.Integer, primary_key=True)
    done_transcoding = db.Column(db.Boolean())
    transcode_timestamp = db.Column(db.DateTime())
    transcode_file_size = db.Column(db.BigInteger())
    original_file_size = db.Column(db.BigInteger())

