import os

import datetime

CHAT_LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d") + '_log.json'

if os.path.exists('log/' + CHAT_LOG_FILE):
    print("HI")

else : print("1")