import paho.mqtt.client as paho
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

message = "a" * SIZE

client = paho.Client()

client.username_pw_set("pjpr", "pjpr")

client.connect("pjpr-pt1.westeurope.cloudapp.azure.com", 1883, 60)
client.loop_start()

times = []

for i in range(0, AMOUNT):
    print(f"{round(time.time() * 1000)}")
    then = time.time()

    pub = client.publish("a", message, qos=0)
    pub.wait_for_publish()

    now = time.time()
    times.append(now - then)
    time.sleep(INTERVAL)

print("Average time to send a message: (sec)", (sum(times) / len(times)) * 1000)

client.loop_stop()
