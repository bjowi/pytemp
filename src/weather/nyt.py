import enum
import requests

import tokens
import utils

nyt_sections = [
    'arts',
    'automobiles',
    'books/review',
    'business',
    'fashion',
    'food',
    'health',
    'home',
    'insider',
    'magazine',
    'movies',
    'nyregion',
    'obituaries',
    'opinion',
    'politics',
    'realestate',
    'science',
    'sports',
    'sundayreview',
    'technology',
    'theater',
    't-magazine',
    'travel',
    'upshot',
    'us',
    'world',
]

def fetch_topstories(section):
    uri = f'https://api.nytimes.com/svc/topstories/v2/{section}.json'
    rd = utils.get_html(uri, f'{section}.html', 3600,
                        params={'api-key': tokens.api_key})
    print(rd)

if __name__ == '__main__':
    fetch_topstories('world')
