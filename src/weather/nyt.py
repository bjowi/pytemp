import enum
import json
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

def fetch_topstories(section, opts):
    uri = f'https://api.nytimes.com/svc/topstories/v2/{section}.json'
    rd = utils.get_html(uri, opts.cachedir / f'{section}.html', 3600,
                        params={'api-key': tokens.api_key})
    return json.loads(rd)


def fetch_newswire(source, section, opts):
    uri = f'https://api.nytimes.com/svc/news/v3/content/{source}/{section}.json'
    rd = utils.get_html(uri, opts.cachedir / f'{source}-{section}.html', 3600,
                        params={'api-key': tokens.api_key})
    return json.loads(rd)
