import requests
import time

import sys
import getopt

SIZE = 1
AMOUNT = 100
INTERVAL = 1
argv = sys.argv[1:]

try:
    options, args = getopt.getopt(argv, "s:a:i:", ["size =", "amount =", "interval ="])
except Exception as e:
    print("-s [SIZE] -a [AMOUT/BITs] -i [INTERVAL SECONDS]")
    exit(0)

for name, value in options:
    if name in ['-s', '--size']:
        SIZE = int(value)
    elif name in ['-a', '--amount']:
        AMOUNT = int(value)
    elif name in ['-i', '--interval']:
        DELAY = int(value)

import urllib3
urllib3.disable_warnings()

send_url = "http://pjpr-pt1.westeurope.cloudapp.azure.com/"
message = "a" * SIZE

for i in range(0, AMOUNT):
    then = time.time()
    response = requests.post(send_url, message, headers={'Content-Type':'application/json'}, verify=False)
    now = time.time()

    print(round(then*1000))
    time.sleep(INTERVAL)
