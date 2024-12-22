VERSION = "0.1"

import sys
import traceback

import fetch
import fetch_station

ret = 1

try:
    # ret = fetch.main()
    ret = fetch_station.main()
except Exception as e:
    traceback.print_exc()

sys.exit(ret)

