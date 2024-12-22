import argparse
import os
import pathlib


def get_options():
    xdg_cache = os.environ.get('XDG_CACHE_HOME')
    if xdg_cache:
        cache_path = pathlib.Path(xdg_cache) / 'bweather'
    else:
        home = os.environ.get('HOME', '')
        cache_path = pathlib.Path(home) / '.cache' / 'bweather'

    parser = argparse.ArgumentParser(
        prog='weather',
        description='Fetch weather data',
        epilog='',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help="Print extra debugging information")
    parser.add_argument('-s', '--station',
                        type=str, required=True,
                        help="ICAO airport code")
    parser.add_argument('--cachedir',
                        type=str, default=cache_path,
                        help="Directory for downloaded files")
    parser.add_argument('--age', type=int, default=604800,
                        help="Wait this long before fetching data again")
    parser.add_argument('--gen-stations',
                        action='store_true',
                        help="Generate station name-id map")

    return parser.parse_args()



