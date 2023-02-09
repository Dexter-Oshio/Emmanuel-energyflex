import paho.mqtt.client as mqtt
import requests


# callback for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print("Message received: " + payload)
    # post data to FlexMeasures
    url = "https://localhost:8000/api/v3_0/sensors/data"
    headers = {
        "Authorization": "Bearer <API_KEY>",
        "Content-Type": "application/json"
    }
    data = {
        "value": payload
    }
    response = requests.post(url, headers=headers, json=data)
    print("Data posted to FlexMeasures with status code: " + str(response.status_code))

# MQTT client setup
client = mqtt.Client()
client.on_message = on_message
client.connect("test.mosquitto.org", 1883, 60)
client.subscribe("iot-data")
client.loop_forever()
