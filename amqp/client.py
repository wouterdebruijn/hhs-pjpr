from uamqp import SendClient, ReceiveClient, Message
from uamqp.constants import MessageState
from urllib import parse

class AMQPProtocol():
    _iot_hub_name: str
    _device_id: str
    _send_client: SendClient
    _receive_client: ReceiveClient

    def __init__(self, device_id: str, sas_token: str, iot_hub_name: str):
        self._iot_hub_name = iot_hub_name
        self._device_id = device_id

        hostname = '{iot_hub_name}.azure-devices.net'.format(iot_hub_name=iot_hub_name)
        username = '{device_id}@sas.{iot_hub_name}'.format(device_id=device_id, iot_hub_name=iot_hub_name)

        send_operation = f'/devices/{device_id}/messages/events'
        send_uri = f'amqps://{parse.quote_plus(username)}:{parse.quote_plus(sas_token)}@{hostname}{send_operation}'

        receive_operation = f'/devices/{device_id}/messages/devicebound'
        receive_uri = f'amqps://{parse.quote_plus(username)}:{parse.quote_plus(sas_token)}@{hostname}{receive_operation}'

        self._send_client = SendClient(send_uri, debug=True)
        self._receive_client = ReceiveClient(receive_uri, debug=True)


    def send_message(self, message: str) -> None:
        # Create message
        msg_data = message.encode('utf-8')

        application_properties = { "app_property_key": "app_property_value" }
        message = Message(msg_data, application_properties=application_properties)

        self._send_client.queue_message(message)
        results = self._send_client.send_all_messages()

        for result in results:
            if result == MessageState.SendFailed:
                raise Exception("Send failed.")

    def receive_message(self) -> str:
        batch = self._receive_client.receive_message_batch(max_batch_size=1)
        for msg in batch:
            print(f"Received: {msg}")
            return msg