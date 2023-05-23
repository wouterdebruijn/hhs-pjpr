import ssl
from paho.mqtt import client as mqtt

class MQTTProtocol():
    _client: mqtt.Client
    _messages: list[str] = []
    _iot_hub_name: str
    _device_id: str

    def __init__(self, device_id: str, sas_token: str, iot_hub_name: str):
        self._iot_hub_name = iot_hub_name
        self._device_id = device_id

        _client = mqtt.Client(client_id=device_id, protocol=mqtt.MQTTv311)

        _client.on_connect = self._on_connect
        _client.on_disconnect = lambda client, userdata, rc: print(f"Device disconnected with result code: {rc}")
        _client.on_publish = lambda client, userdata, mid: print("Device sent message")
        _client.on_message = self.on_message

        _client.username_pw_set(username=f"{iot_hub_name}.azure-devices.net/{device_id}/?api-version=2021-04-12", password=sas_token)
        _client.tls_set(certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
        _client.tls_insecure_set(False)

        self._client = _client

    def on_message(self, client, userdata, message):
        self._messages.append(message.payload.decode("utf-8"))

    def send_message(self, message: str) -> None:
        mqtt_info = self._client.publish(f"devices/{self._device_id}/messages/events/", message)

    def receive_message(self) -> str:
        # Wait for a message to be received
        self._client.loop_start()
        while len(self._messages) == 0:
            pass
        self._client.loop_stop()

        # Return the first message in the list
        return self._messages.pop(0)
        

    def _on_connect(self, client, userdata, flags, rc):
        print(f"Device connected with result code: {rc}")

        # Subscribe to the topic that contains messages sent from the cloud to the device
        self._client.subscribe(f"devices/{self._device_id}/messages/devicebound/#")

    def connect(self) -> None:
        self._client.connect(self._iot_hub_name+".azure-devices.net", port=8883)