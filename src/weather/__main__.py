VERSION = "0.1"

import sys
import traceback

import fetch

ret = 1
try:
    ret = fetch.main()
except Exception as e:
    traceback.print_exc()

sys.exit(ret)

