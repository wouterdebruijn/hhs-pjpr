import ssl
from paho.mqtt import client as mqtt
import sys

device_id = "pjpr-device-1"
# Read SAS Token from command line argument
sas_token = sys.argv[1] 
iot_hub_name = "pjpr-iothub"

def on_connect(client, userdata, flags, rc):
    print("Device connected with result code: " + str(rc))


def on_disconnect(client, userdata, rc):
    print("Device disconnected with result code: " + str(rc))


def on_publish(client, userdata, mid):
    print("Device sent message")

def on_message(client, userdata, message):
    print("Message received: " + str(message.payload))


client = mqtt.Client(client_id=device_id, protocol=mqtt.MQTTv311)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.on_message = on_message

client.username_pw_set(username=iot_hub_name+".azure-devices.net/" +
                       device_id + "/?api-version=2021-04-12", password=sas_token)

client.tls_set(certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
client.tls_insecure_set(False)

client.connect(iot_hub_name+".azure-devices.net", port=8883)

# Send message from device to cloud
client.publish("devices/" + device_id + "/messages/events/", '{"id":123}', qos=1)

# https://learn.microsoft.com/en-us/azure/iot/iot-mqtt-connect-to-iot-hub?toc=%2Fazure%2Fiot-hub%2Ftoc.json&bc=%2Fazure%2Fiot-hub%2Fbreadcrumb%2Ftoc.json#receiving-cloud-to-device-messages
# Receive messages sent to device
client.subscribe("devices/" + device_id + "/messages/devicebound/#", qos=1)

client.loop_forever()