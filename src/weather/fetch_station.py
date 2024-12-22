#!/bin/python3

import options
import parsers
import smhi
import utils


files = {
    "malmen_temp.json": {
        'url': smhi.get_smhi_url,
        'parameter': 1,
        'age': 3600,
        'parse_fun': parsers.parse_smhi,
        'type': 'SMHI',
    },
    "malmen_weather.json": {
        'url': smhi.get_smhi_url,
        'parameter': 13,
        'age': 3600,
        'parse_fun': parsers.parse_smhi,
        'type': 'SMHI',
    },
}


def main():
    opts = options.get_options()

    opts.cachedir.mkdir(parents=True, exist_ok=True)

    if opts.gen_stations:
        utils.gen_station_map(opts.cachedir / "malmen_temp.json")
        return 0

    station = utils.translate_station(opts.station)

    for filename, fdata in files.items():
        if fdata.get('disabled'):
            continue

        url = fdata['url'](opts.station, fdata['parameter'])
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

    outputs = []
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
                outputs.append(f"{stations.get(opts.station)}")

    print(' '.join(outputs))
    return 0
