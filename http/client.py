import requests
import time

class HTTPProtocol():
	_iot_hub_name: str
	_device_id: str
	_Azure_api_version = '2020-03-13'
	_sas_token: str
	_polling_rate = 1 #in seconden

	def __init__(self, device_id: str, sas_token: str, iot_hub_name: str):
		self._iot_hub_name = iot_hub_name
		self._device_id = device_id
		self._Azure_api_version = api_version
		self._sas_token = sas_token

	def send_message(self, message: str) -> None:
		send_url = f'https://{self._iot_hub_name}.azure-devices.net/devices/{self._device_id}/messages/events?api-version={self._Azure_api_version}'
		response = requests.post(send_url, message, headers={'Content-Type':'application/json',
															'Authorization': self._sas_token})
		if(response.status_code != 200):
			raise Exception(f'Het versturen van het bericht is niet gelukt. status_code:{response.status_code}')

	def receive_message(self) -> str:
		receive_url = f'https://{self._iot_hub_name}.azure-devices.net/devices/{self._device_id}/messages/deviceBound?api-version={self._Azure_api_version}'

		response = null
		while(response.status_code != 200):
			response = requests.get(receive_url, headers={'Content-Type':'application/json',
														'Authorization': self._sas_token})
			time.sleep(self._polling_rate)

		message = response.text

		response = requests.get(receive_url, headers={'Content-Type':'application/json',
													'Authorization': self._sas_token})
		ETag = response.headers.get('ETag')
		ETag = ETag.strip('"')
		delete_url = f'https://{self._iot_hub_name}.azure-devices.net/devices/{self._device_id}/messages/deviceBound/{ETag}?api-version={self._Azure_api_version}'
		response = requests.delete(delete_url, headers={'Authorization': self._sas_token})

		return message

	def connect(self) -> None:
		pass