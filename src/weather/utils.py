import calendar
import datetime
import json
import locale
import os
import time

import requests

import constants
import stations


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
    elif station in stations.smhi_name_to_station:
        return stations.smhi_name_to_station[station]['key']
    else:
        return station


def get_dayname():
    locale.setlocale(locale.LC_ALL, '')
    now = datetime.datetime.now()
    weekday = calendar.weekday(now.year, now.month, now.day)
    return calendar.day_abbr[weekday]


def gen_station_map(filename):
    smhi_name_to_station = {}
    smhi_key_to_station = {}
    with open(filename, 'r') as f:
        data = json.load(f)
        for station in data['station']:
            smhi_key_to_station[station['key']] = station
            smhi_name_to_station[station['name']] = station

    with open('stations.py', 'w') as f:
        f.write(f'smhi_name_to_station = {smhi_name_to_station}\n')
        f.write(f'smhi_key_to_station = {smhi_key_to_station}\n')
