import logging
import asyncio
import time
import sys
import getopt

from aiocoap import *

logging.basicConfig(level=logging.INFO)

SIZE = 1
AMOUNT = 100
INTERVAL = 1
argv = sys.argv[1:]

try:
    options, args = getopt.getopt(argv, "s:a:i:",
                               ["size =",
                                "amount =",
                                "interval ="])
except Exception as e:
    print("-s [SIZE] -a [AMOUT/BITs] -i [INTERVAL SECONDS]")
    print(e)

for name, value in options:
    if name in ['-s', '--size']:
        SIZE = int(value)
    elif name in ['-a', '--amount']:
        AMOUNT = int(value)
    elif name in ['-i', '--interval']:
        DELAY = int(value)

async def main():
    print("Preforming CoAP Test")
    protocol = await Context.create_client_context()

    msg = "a" * SIZE
    for x in range(1, AMOUNT + 1):
        try:
            print(str(round(time.time() * 1000)))
            request = Message(code=GET, uri='coap://pjpr-pt1.westeurope.cloudapp.azure.com/time', payload=bytes(msg, 'utf-8'))
            request.payload = bytes(msg, 'utf-8')
            response = await protocol.request(request).response
        except Exception as e:
            print('Failed to fetch resource:')
            print(e)

        time.sleep(INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
