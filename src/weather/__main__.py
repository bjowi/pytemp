VERSION = "0.1"

import sys
import traceback

import fetch_smhi

ret = 1

try:
    ret = fetch_smhi.main()
except Exception as e:
    traceback.print_exc()

sys.exit(ret)

