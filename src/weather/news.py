import datetime
import json
import operator
import sys
import time
import traceback

import nyt
import options
import utils

from pprint import pprint

from static import make_html


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
            match opts.format:
                case 'text':
                    print(f"{topstory['title'][:100]}")
                case 'html':
                    stories = []
                    footer = f'<a href="https://developer.nytimes.com/"><img src="poweredby_nytimes_200a.png" /></a>'
                    for story in world:
                        #print(story)
                        stories.append(f'<h1><a href="{story["url"]}">{story["title"][:200]}</a></h1>\n')
                    print(make_html(title='News',
                                    heading=f'News from <a href="https://www.nytimes.com/">The New York Times</a>, updated {time.ctime(time.time())}',
                                    body='\n'.join(stories),
                                    footer=footer))
                case 'yuck':
                    headlines = []
                    for story in world:
                        headlines.append(f"(expander :name '{story['title']}'"
                                         f"(box :orientation 'h'"
                                         f"(label :halign 'start' :width 70 :wrap true :text '{story['abstract']}' :class 'headline')"
                                         f"(button :class 'link' :onclick 'firefox {story['url']} && eww close news')))")

                    news = (f"(box :orientation 'v' :class 'news' :space-evenly false {'\n'.join(headlines)})")
                    print(news)

        return 0
    except Exception:
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
