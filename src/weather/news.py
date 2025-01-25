import datetime
import json
import operator
import sys
import traceback

import nyt
import options
import utils

from pprint import pprint


def datesort(e):
    return datetime.datetime.fromisoformat(e['updated_date'])


def main():
    try:
        opts = options.get_news_options()
        opts.cachedir.mkdir(parents=True, exist_ok=True)

        if opts.site == 'nyt':
            world = nyt.fetch_topstories(opts.section, opts).get('results')
            newswire = nyt.fetch_newswire(opts.source, opts.section, opts).get('results')
            topstory = sorted(world, key=datesort)[-1]
            print(f"{topstory['title'][:100]}")

        return 0
    except Exception:
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
