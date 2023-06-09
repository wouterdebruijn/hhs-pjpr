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
    protocol.client_credentials.load_from_dict({"coaps://13.80.102.200/time": {"dtls": {"psk": {"ascii": "11223344"}, "client-identity": {"ascii": "client_Identity"}}}})

    msg = "a" * SIZE

    start = time.time()
    request = Message(code=GET, uri='coaps://13.80.102.200/time', payload=bytes(msg, 'utf-8'))

    print(len(msg.encode('utf-8')))

    for x in range(1, AMOUNT + 1):
        try:
            print("Sending Message - ", x)
            print("Sending CON at: " + str(round(time.time() * 1000)))

            request.payload = bytes(msg * x, 'utf-8')
            response = await protocol.request(request).response

            time.sleep(INTERVAL)
            #async for r in response.observation:
                #print("Next result: %s\n%r"%(r, r.payload))

                #response.observation.cancel()
                #break

        except Exception as e:
            print('Failed to fetch resource:')

            print(e)

        else:
            # print(f'TimeLocal: {(time.time() - start) * 1000} ms')
            # print(f'TimeServer: {(float(response.payload) - start) * 1000} ms')
            print(response.payload)

            print("Received ACK at: " + str(round(time.time() * 1000)))

        time.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
