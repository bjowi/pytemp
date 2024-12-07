#!/bin/python3

import options
import parsers
import utils


files = {
    "metar_norden.html": {
        'disabled': True,
        'url': "https://aro.lfv.se/Links/Link/ViewLink?TorLinkId=300&type=MET",
        'age': 18000,
        'parse_fun': parsers.parse_aro,
        'type': 'METAR',
    },
    "taf_norden.html": {
        'disabled': True,
        'url': "https://aro.lfv.se/Links/Link/ViewLink?TorLinkId=304&type=MET",
        'age': 18000,
        'parse_fun': parsers.parse_aro,
        'type': 'TAF',
    },
    "malmen_temp.json": {
        'url': "https://opendata-download-metobs.smhi.se/api/version/latest/parameter/1/station-set/all/period/latest-hour/data.json",
        'age': 3600,
        'parse_fun': parsers.parse_smhi,
        'type': 'SMHI',
    },
}


def main():
    opts = options.get_options()

    opts.cachedir.mkdir(parents=True, exist_ok=True)

    station = utils.translate_station(opts.station)

    for filename, fdata in files.items():
        if fdata.get('disabled'):
            continue

        url = fdata['url']
        age = fdata['age']
        if not age:
            age = opts.age
        fdata['data'] = utils.get_html(url, opts.cachedir / filename, age, opts.verbose)
        match fdata['type']:
            case 'METAR':
                fdata['stations'] = fdata['parse_fun'](fdata['data'])
            case 'TAF':
                fdata['stations'] = fdata['parse_fun'](fdata['data'])
            case 'SMHI':
                fdata['stations'] = fdata['parse_fun'](fdata['data'])

    tempsd = {}
    for filename, fdata in files.items():
        if fdata.get('disabled'):
            continue

        stations = fdata['stations']
        if opts.verbose:
            for k in sorted(stations.keys()):
                print(f"{k}: {stations[k]}")

        match fdata['type']:
            case 'METAR':
                metar = stations.get(station)
                if metar:
                    # this works for malmen. the formats are otherwise inconsistent
                    temp, dewpoint = metar.split(' ')[-2].replace('M', '-').split('/')
                    print(temp, dewpoint)
            case 'SMHI':
                print(f"{stations.get(station)}")
