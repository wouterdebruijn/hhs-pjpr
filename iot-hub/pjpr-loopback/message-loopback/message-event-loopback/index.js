// Get message from device and send it back to the device
// This function is triggered by an Event Grid event when a message is sent to the IoT Hub
// The message is sent back to the device using the IoT Hub SDK

const Client = require('azure-iothub').Client;

const client = Client.fromConnectionString(process.env['IOTHUB_CONNECTION_STRING']);

module.exports = async function (context, eventGridEvent) {
    context.log(eventGridEvent);

    if (eventGridEvent.eventType !== 'Microsoft.Devices.DeviceTelemetry') {
        context.done();
        return;
    }

    const deviceId = eventGridEvent.data.systemProperties['iothub-connection-device-id'];
    const messageBase64 = eventGridEvent.data.body;

    const message = Buffer.from(messageBase64, 'base64').toString('ascii');

    await client.send(deviceId, message);

    context.done();
};