import requests

from datetime import datetime
from decimal import Decimal


class TmdbService(object):

    BASE_URL = 'https://api.themoviedb.org/3/movie'
    API_KEY = '0cc618d6f56c44414a4f82520b76f45f'

    @staticmethod
    def get_movie_details(tmdb_id):
        get_json_response = TmdbService._get(tmdb_id)
        return {
            'title_name': get_json_response['original_title'],
            'release_year': datetime.strptime(get_json_response['release_date'], '%Y-%m-%d').year,
            'film_rating': '',
            'runtime': int(get_json_response['runtime']),
            'genres': ','.join([genre['name'] for genre in get_json_response['genres']]),
            'poster_artwork': get_json_response['poster_path'],
            # 'rating': Decimal(str(get_json_response['vote_average'])),
            'rating': str(get_json_response['vote_average']),
        }

    @staticmethod
    def _get(tmdb_id):
        get_response = requests.get(
            url=f'{TmdbService.BASE_URL}/{tmdb_id}?api_key={TmdbService.API_KEY}',
            headers={'Content-Type': 'application/json;charset=utf-8'}
        )
        return get_response.json()
