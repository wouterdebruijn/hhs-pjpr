import logging
import asyncio
import time

from aiocoap import *

logging.basicConfig(level=logging.INFO)

async def main():
    print("Preforming CoAP Test")
    protocol = await Context.create_client_context()
    protocol.client_credentials.load_from_dict({"coaps://13.80.102.200/time": {"dtls": {"psk": {"ascii": "11223344"}, "client-identity": {"ascii": "client_Identity"}}}})

    start = time.time()
    request = Message(code=GET, uri='coaps://13.80.102.200/time')

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        # print(f'TimeLocal: {(time.time() - start) * 1000} ms')
        # print(f'TimeServer: {(float(response.payload) - start) * 1000} ms')
        print(response.payload)


if __name__ == "__main__":
    asyncio.run(main())
