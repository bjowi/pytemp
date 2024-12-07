VERSION = "0.1"

from .fetch import main

ret = 1
try:
    ret = main()
except Exception as e:
    print(f"Error: {str(e)}")

sys.exit(ret)

