from amqp.client import AMQPProtocol
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

    # protocol = MQTTProtocol(device_id, sas_token, iot_hub_name)
    # protocol.connect()

    protocol = AMQPProtocol(device_id, sas_token, iot_hub_name)

    # Run the test
    run_test(protocol)

def run_test(protocol):
    
    print("Starting test...")

    for i in range(5):
        start_time = time.time()
        protocol.send_message("Hello from Python!")
        print(protocol.receive_message())
        print(f"Message time in milliseconds: {(time.time() - start_time) * 1000}")
        
        time.sleep(1)
        
    print("Test complete.")


__main__ = main()