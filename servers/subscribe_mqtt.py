import paho.mqtt.client as paho
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with result code:", str(rc))

client = paho.Client()
client.on_connect = on_connect

client.username_pw_set("pjpr", "pjpr")

client.connect("localhost", 1883, 60)

def on_connect(client, userdata, flags, rc):
	print("connected")
	client.subscribe("#")

def on_message(client, userdata, message):
	print(round(time.time() * 1000))

client.on_message = on_message
client.on_connect = on_connect

client.loop_forever()