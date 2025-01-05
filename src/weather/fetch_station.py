#!/bin/python3

import options
import parsers
import smhi
import utils


files = {
    'temp.json': {
        'parameter': 1,
    },
    'weather.json': {
        'parameter': 13,
    },
}


def main():
    opts = options.get_options()

    opts.cachedir.mkdir(parents=True, exist_ok=True)

    if opts.gen_stations:
        utils.gen_station_map(opts.cachedir / 'stations.json')
        return 0

    if opts.list_stations:
        for s in utils.get_stations():
            print(s)
        return 0

    station = utils.translate_station(opts.station)

    for param_name, fdata in files.items():
        if fdata.get('disabled'):
            continue

        filename = opts.cachedir / f'{station}-{param_name}'
        fdata['filename'] = filename

        url = smhi.get_smhi_url(opts.station, fdata['parameter'])
        fdata['data'] = utils.get_html(url, filename, opts.age, opts.verbose)
        fdata['stations'] = parsers.parse_smhi(fdata['data'])

    outputs = []
    for param_name, fdata in files.items():
        if fdata.get('disabled'):
            continue

        filename = fdata['filename']
        stations = fdata['stations']
        if opts.verbose:
            for k in sorted(stations.keys()):
                print(f"{k}: {stations[k]}")

        data = stations.get(opts.station)
        parameter = fdata['parameter']

        match parameter:
            case 13:
                if opts.describe_weather:
                    weather = utils.get_weather_description(int(data))
                    if weather:
                        outputs.append(weather)
                    else:
                        print(f"Weather type {data} not found")
                        return 2
                else:
                    outputs.append(f"{data}")
            case 1:
                outputs.append(f"{data}°C")
            case _:
                outputs.append(f"{data}")

    print(' '.join(outputs))
    return 0
