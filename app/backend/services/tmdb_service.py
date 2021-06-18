import requests

from datetime import datetime
from decimal import Decimal


class TmdbService(object):

    API_BASE_URL = 'https://api.themoviedb.org'
    API_VERSION = 3
    FIND_MOVIE_USING_IMDB_ID_BASE_URL = f'{API_BASE_URL}/{API_VERSION}/find/{{imdb_id}}'
    MOVIE_DETAILS_BASE_URL = f'{API_BASE_URL}/{API_VERSION}/movie/{{tmdb_id}}'
    API_KEY = '0cc618d6f56c44414a4f82520b76f45f'

    POSTER_BASE_URL = 'http://image.tmdb.org/t/p'
    POSTER_SIZE = 'w92'

    @staticmethod
    def get_movie_details(imdb_id):
        find_movie_details = TmdbService._api_find_movie_using_imdb_id(imdb_id=imdb_id)
        tmdb_id = find_movie_details['id']
        movie_data = TmdbService._api_get_movie_details(tmdb_id=tmdb_id)
        return {
            'imdb_id': imdb_id,
            'tmdb_id': tmdb_id,
            'title_name': movie_data['original_title'],
            'release_year': datetime.strptime(movie_data['release_date'], '%Y-%m-%d').year,
            'film_rating': '',
            'runtime': movie_data['runtime'],
            'genres': ','.join([genre['name'] for genre in movie_data['genres']]),
            'poster_artwork': f"{TmdbService.POSTER_BASE_URL}/{TmdbService.POSTER_SIZE}/{movie_data['poster_path']}",
            'rating': Decimal(str(movie_data['vote_average']))
        }

    @staticmethod
    def _api_find_movie_using_imdb_id(imdb_id):
        query_params = {'external_source': 'imdb_id'}
        response = TmdbService._get(TmdbService.FIND_MOVIE_USING_IMDB_ID_BASE_URL.format(imdb_id=imdb_id), query_params)
        movie_results = response['movie_results']
        if len(movie_results) == 0:
            raise requests.exceptions.HTTPError(f'Movie With IMDB ID: ({imdb_id}) Not Found')
        return movie_results[0]

    @staticmethod
    def _api_get_movie_details(tmdb_id):
        response = TmdbService._get(TmdbService.MOVIE_DETAILS_BASE_URL.format(tmdb_id=tmdb_id))
        if 'success' in response and not response['success']:
            raise requests.exceptions.HTTPError(f'Movie With TMDB ID: ({tmdb_id}) Not Found')
        return response

    @staticmethod
    def _get(url, query_params=None):
        if not query_params:
            query_params = {}
        query_params['api_key'] = TmdbService.API_KEY
        get_response = requests.get(
            url=f'{url}', params=query_params, headers={'Content-Type': 'application/json;charset=utf-8'}
        )
        get_response.raise_for_status()
        return get_response.json()
