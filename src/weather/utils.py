import calendar
import datetime
import locale
import os
import time

import requests

import constants


def file_is_current(filename, age=604800):
    try:
        file_age = time.time() - os.stat(filename).st_mtime
        if file_age >= age:
            return False
        else:
            return True
    except FileNotFoundError:
        return False


def get_html(url, filename, age, verbose=False):
    if file_is_current(filename, age=age):
        if verbose:
            print(f'Already have current {filename}')
        with open(filename) as htmlfile:
            html = htmlfile.read()
    else:
        if verbose:
            print(f'Fetching new html from {url}')
        rd = requests.get(url,
                          headers={
                              'Accept-Language': 'en-US',
                              'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0'
                          },
                          verify=True)
        html = rd.text
        with open(filename, 'w') as f:
            f.write(html)

    return html


def translate_station(station):
    if station in constants.icao_to_station_name:
        return constants.icao_to_station_name[station]
    elif station in constants.smhi_key_to_station_name:
        return constants.smhi_key_to_station_name[station]
    else:
        return station


def get_dayname():
    locale.setlocale(locale.LC_ALL, '')
    now = datetime.datetime.now()
    weekday = calendar.weekday(now.year, now.month, now.day)
    return calendar.day_abbr[weekday]
