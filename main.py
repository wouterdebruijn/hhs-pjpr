from mqtt.client import MQTTProtocol
from yaml import load, Loader

import time

def main():
    config = {}

    with open("./device.yaml", "r") as file:
        config = load(file, Loader=Loader)

    device_id = config["device_id"]
    sas_token = config["sas_token"]
    iot_hub_name = config["iot_hub_name"]

    protocol = MQTTProtocol(device_id, sas_token, iot_hub_name)
    protocol.connect()

    for i in range(5):
        start_time = time.time()
        protocol.send_message("Hello from Python!")
        print(protocol.receive_message())
        print(f"Message time in milliseconds: {(time.time() - start_time) * 1000}")\
        
        time.sleep(1)


__main__ = main()