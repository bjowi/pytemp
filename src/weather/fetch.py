#!/bin/python3

import calendar
import datetime
import locale
import os
import time

import requests

from . import options
from . import parsers


files = {
    "metar_norden.html": {
        'url': "https://aro.lfv.se/Links/Link/ViewLink?TorLinkId=300&type=MET",
        'age': 18000,
        'parse_fun': parsers.parse_aro,
        'type': 'METAR',
    },
    "taf_norden.html": {
        'url': "https://aro.lfv.se/Links/Link/ViewLink?TorLinkId=304&type=MET",
        'age': 18000,
        'parse_fun': parsers.parse_aro,
        'type': 'TAF',
    },
}


def file_is_current(filename, age=604800):
    try:
        file_age = time.time() - os.stat(filename).st_mtime
        if file_age >= age:
            return False
        else:
            return True
    except FileNotFoundError:
        return False


def get_html(url, filename, opts):
    if file_is_current(filename, age=opts.age):
        if opts.verbose:
            print(f'Already have current {filename}')
        with open(filename) as htmlfile:
            html = htmlfile.read()
    else:
        print(f'Fetching new html from {url}')
        rd = requests.get(url,
                          headers={
                              'Accept-Language': 'en-US',
                              'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0'
                          },
                          verify=False)
        html = rd.text
        with open(filename, 'w') as f:
            f.write(html)

    return html


def get_dayname():
    locale.setlocale(locale.LC_ALL, '')
    now = datetime.datetime.now()
    weekday = calendar.weekday(now.year, now.month, now.day)
    return calendar.day_abbr[weekday]


def main():
    opts = options.get_options()

    for filename, fdata in files.items():
        url = fdata['url']
        age = fdata['age']
        fdata['data'] = get_html(url, filename, opts)
        fdata['stations'] = fdata['parse_fun'](fdata['data'])

    for filename, fdata in files.items():
        stations = fdata['stations']
        if opts.verbose:
            for k in sorted(stations.keys()):
                print(f'{k}: {stations[k]}')

        print(f'{opts.station} {fdata['type']}: {stations.get(opts.station)}')
