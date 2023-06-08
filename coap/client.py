import logging
import asyncio
import time

from aiocoap import *

logging.basicConfig(level=logging.INFO)

async def main():
    print("Preforming CoAP Test")
    protocol = await Context.create_client_context()
    protocol.client_credentials.load_from_dict({"coaps://13.80.102.200/tim": {"dtls": {"psk": {"ascii": "11223344"}, "client-identity": {"ascii": "client_Identity"}}}})

    start = time.time()
    request = Message(code=GET, uri='coaps://13.80.102.200/tim')

    msg = "a" * 1048576 * 10
    print(len(msg.encode('utf-8')))


    for x in range(0, 1):
        try:
            print("Sending Message - ", x)
            response = await protocol.request(request).response
        except Exception as e:
            print('Failed to fetch resource:')
            print(e)
        else:
            # print(f'TimeLocal: {(time.time() - start) * 1000} ms')
            # print(f'TimeServer: {(float(response.payload) - start) * 1000} ms')
            print(response.payload)
            print(round(time.time() * 1000))
        time.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
