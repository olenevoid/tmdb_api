import requests
from getpass import getpass
import os


def make_tmdb_api_request(method, api_key, extra_params=None):
    extra_params = extra_params or {}
    url = 'http://api.themoviedb.org/3%s' % method
    params = {
        'api_key': api_key,
        'language': 'ru',
    }
    params.update(extra_params)
    return load_json_data_from_url(url, params)


def load_json_data_from_url(base_url, url_params):
    proxy = get_proxy()
    proxies = {}
    
    if proxy is not None:
        proxies['http'] = 'http://%s' % get_proxy()
    
    response = requests.get(base_url, params=url_params, proxies=proxies)
    return response.json()


def get_user_api_key():
    user_api_key = getpass('Enter your api key v3:')
    try:
        make_tmdb_api_request(method='/movie/2', api_key = user_api_key)
        return user_api_key
    except requests.exceptions.HTTPError as err:
        if err.code == 401:
            return None
        else:
            raise


def get_proxy():
    proxy_file = 'proxy.txt'
    if os.path.exists(proxy_file):
        with open(proxy_file, 'r') as file:
            return file.readline()
        
    return None
