from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, Integer, Numeric, SmallInteger, String
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://app:postgres@db:5432/app"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

Base = declarative_base()


class TranscodingMetadata(Base):
    __tablename__ = 'transcoding_metadata'

    tmdb_id = Column(Integer, primary_key=True)
    done_transcoding = Column(Boolean())
    transcode_timestamp = Column(DateTime())
    transcode_file_size = Column(BigInteger())
    original_file_size = Column(BigInteger())


class TmdbMetadata(Base):
    __tablename__ = 'tmdb_metadata'

    tmdb_id = Column(Integer, primary_key=True)
    title_name = Column(String(256))
    release_year = Column(Date())
    film_rating = Column(String(12))
    runtime = Column(SmallInteger())
    genres = Column(String(256))
    poster_artwork = Column(String(256))
    rating = Column(Numeric())
