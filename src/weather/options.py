import argparse
import os


def get_options():
    home = os.environ.get('HOME', '')

    parser = argparse.ArgumentParser(
        prog='weather',
        description='Fetch weather data',
        epilog='',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help="Print extra debigging information")
    parser.add_argument('-s', '--station',
                        type=str, required=True,
                        help="ICAO airport code")
    parser.add_argument('--cachedir',
                        type=str, default=f'{home}/.cache',
                        help="Directory for downloaded files")
    parser.add_argument('--age', type=int, default=604800,
                        help="Wait this long before fetching data again")
    return parser.parse_args()



