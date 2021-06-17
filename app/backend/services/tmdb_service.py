import requests

from datetime import datetime
from decimal import Decimal


class TmdbService(object):

    BASE_URL = 'https://api.themoviedb.org/3/find'
    API_KEY = '0cc618d6f56c44414a4f82520b76f45f'

    @staticmethod
    def get_movie_details(imdb_id):
        get_json_response = TmdbService._get(imdb_id)
        movie_results = get_json_response['movie_results']
        if len(movie_results) == 0:
            raise Exception('not found')
        movie_data = movie_results[0]
        return {
            'imdb_id': imdb_id,
            'title_name': movie_data['title'],
            'release_year': datetime.strptime(movie_data['release_date'], '%Y-%m-%d').year,
            'film_rating': '',
            'runtime': 0,
            # 'genres': ','.join([genre['name'] for genre in get_json_response['genre_ids']]),
            'genres': '',
            'poster_artwork': movie_data['poster_path'],
            # 'rating': Decimal(str(get_json_response['vote_average'])),
            'rating': movie_data['vote_average'],
        }

    @staticmethod
    def _get(imdb_id):
        get_response = requests.get(
            url=f'{TmdbService.BASE_URL}/{imdb_id}',
            params={'external_source': 'imdb_id', 'api_key': TmdbService.API_KEY},
            headers={'Content-Type': 'application/json;charset=utf-8'}
        )
        get_response.raise_for_status()
        return get_response.json()
