import argparse
import os
import pathlib


def get_common_options(parser):
    xdg_cache = os.environ.get('XDG_CACHE_HOME')
    if xdg_cache:
        cache_path = pathlib.Path(xdg_cache) / 'bweather'
    else:
        home = os.environ.get('HOME', '')
        cache_path = pathlib.Path(home) / '.cache' / 'bweather'

    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help="Print extra debugging information")
    parser.add_argument('--cachedir',
                        type=str, default=cache_path,
                        help="Directory for downloaded files")
    parser.add_argument('--age', type=int, default=3600,
                        help="Wait this long before fetching data again")


def get_weather_options():
    parser = argparse.ArgumentParser(
        prog='weather',
        description='Fetch weather data',
        epilog='',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    get_common_options(parser)

    parser.add_argument('-i', '--icao',
                        type=str,
                        default='ESCF',
                        help="ICAO airport code")
    parser.add_argument('-s', '--station',
                        type=str,
                        default='Linköping-Malmslätt',
                        help="SMHI station name")
    parser.add_argument('-w', '--describe-weather',
                        action='store_true',
                        required=False,
                        help="Explain an SMHI weather code")
    parser.add_argument('--gen-stations',
                        action='store_true',
                        help="Generate station name-id map")
    parser.add_argument('--list-stations',
                        action='store_true',
                        help="Print station names")

    return parser.parse_args()


def get_news_options():
    parser = argparse.ArgumentParser(
        prog='news',
        description='Fetch enws headlines',
        epilog='',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--site',
                        type=str,
                        required=False,
                        default='nyt',
                        help="nyt, guardian, lemonde, etc.")

    parser.add_argument('--source',
                        type=str,
                        required=False,
                        default='all',
                        help="News source (nyt terminology)")

    parser.add_argument('--section',
                        type=str,
                        required=False,
                        default='world',
                        help="News section")

    get_common_options(parser)

    return parser.parse_args()
