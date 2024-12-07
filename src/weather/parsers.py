import json

from bs4 import BeautifulSoup

import utils

def parse_aro(html):

    soup = BeautifulSoup(html, 'html.parser')

    stations = {}
    for row in soup.find_all(class_="tor-link-text-row"):
        items = row.find_all(class_="tor-link-text-row-item")
        ki, vi = items
        if ki.text:
            station = utils.translate_station(ki.text)
            stations[station] = vi.text

    return stations

def parse_smhi(html):
    data = json.loads(html)
    res = {}
    for station in data.get('station', []):
        value = station.get('value')
        if value:
            res[station['name']] = value[0]['value']

    return res
