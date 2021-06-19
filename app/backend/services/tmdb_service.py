import requests

from datetime import datetime
from decimal import Decimal


class TmdbService(object):
    '''
    Service that acts as a wrapper that interacts with the TMDB API
    '''

    API_BASE_URL = 'https://api.themoviedb.org'
    API_VERSION = 3
    FIND_MOVIE_USING_IMDB_ID_BASE_URL = f'{API_BASE_URL}/{API_VERSION}/find/{{imdb_id}}'
    MOVIE_DETAILS_BASE_URL = f'{API_BASE_URL}/{API_VERSION}/movie/{{tmdb_id}}'
    API_KEY = 'XXXXX'

    POSTER_BASE_URL = 'http://image.tmdb.org/t/p'
    POSTER_SIZE = 'w92'

    @staticmethod
    def get_movie_details(imdb_id):
        '''
        Fetches movie details using the IMDB ID of a movie.
        It follows the steps of:
          1) Using the IMDB ID to find the corresponding TMDB movie. Using the IMDB ID to find the TMDB movie
            yields some movie-details but not all the ones we want.
          2) Fetches the TMDB ID to get more rich movie-detail information from the TMDB API.
          3) Uses the TMDB ID to get the movie information from the TMDB API and builds a JSON response with
            relevant movie details.

        :param imdb_id: The IMDB ID of the movie that you want to get details for
        :type imdb_id: str
        :return: dict
        '''
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
        '''
        Helper function to interact with the API that finds the TMDB movie using the IMDB ID

        :param imdb_id: The IMDB ID of the movie that you want to get details for
        :type imdb_id: str
        :return: dict
        '''
        query_params = {'external_source': 'imdb_id'}
        response = TmdbService._get(TmdbService.FIND_MOVIE_USING_IMDB_ID_BASE_URL.format(imdb_id=imdb_id), query_params)
        movie_results = response['movie_results']
        if len(movie_results) == 0:
            raise requests.exceptions.HTTPError(f'Movie With IMDB ID: ({imdb_id}) Not Found')
        return movie_results[0]

    @staticmethod
    def _api_get_movie_details(tmdb_id):
        '''
        Helper function to interact with the API that fetches the movie details from TMDB using the TMDB ID

        :param tmdb_id: The TMDB ID of the movie that you want to get details for
        :type tmdb_id: str
        :return: dict
        '''
        response = TmdbService._get(TmdbService.MOVIE_DETAILS_BASE_URL.format(tmdb_id=tmdb_id))
        if 'success' in response and not response['success']:
            raise requests.exceptions.HTTPError(f'Movie With TMDB ID: ({tmdb_id}) Not Found')
        return response

    @staticmethod
    def _get(url, query_params=None):
        '''
        Helper method to query the API

        :param url: API URL to hit
        :param url: str
        :param query_params: query-string params of the request
        :param query_params: dict
        :return: dict
        '''
        if not query_params:
            query_params = {}
        query_params['api_key'] = TmdbService.API_KEY
        get_response = requests.get(
            url=f'{url}', params=query_params, headers={'Content-Type': 'application/json;charset=utf-8'}
        )
        get_response.raise_for_status()
        return get_response.json()
