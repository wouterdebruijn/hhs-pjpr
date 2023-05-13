import uamqp
import sys

from urllib import parse

iot_hub_name = 'pjpr-iothub'
hostname = '{iot_hub_name}.azure-devices.net'.format(iot_hub_name=iot_hub_name)
device_id = 'pjpr-device-1'
username = '{device_id}@sas.{iot_hub_name}'.format(device_id=device_id, iot_hub_name=iot_hub_name)
sas_token = sys.argv[1]

# ...
# Create a send client for the device-to-cloud send link on the device
operation = '/devices/{device_id}/messages/events'.format(device_id=device_id)
uri = 'amqps://{}:{}@{}{}'.format(parse.quote_plus(username), parse.quote_plus(sas_token), hostname, operation)

print(uri)

send_client = uamqp.SendClient(uri, debug=True)

# Set any of the applicable message properties
# msg_props = uamqp.message.MessageProperties()
# msg_props.message_id = str(uuid.uuid4())
# msg_props.creation_time = None
# msg_props.correlation_id = None
# msg_props.content_type = 'application/json;charset=utf-8'
# msg_props.reply_to_group_id = None
# msg_props.subject = None
# msg_props.user_id = None
# msg_props.group_sequence = None
# msg_props.to = None
# msg_props.content_encoding = None
# msg_props.reply_to = None
# msg_props.absolute_expiry_time = None
# msg_props.group_id = None

# Application properties in the message (if any)
application_properties = { "app_property_key": "app_property_value" }

# Create message
msg_data = b"Your message payload goes here"
message = uamqp.Message(msg_data, 
                        # properties=msg_props, 
                        application_properties=application_properties)

send_client.queue_message(message)
results = send_client.send_all_messages()

for result in results:
    if result == uamqp.constants.MessageState.SendFailed:
        print(result)