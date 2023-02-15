import paho.mqtt.client as mqtt
import requests
import gettoken
import datetime

# Get the token
token = gettoken.get_token()
auth_token = "" + token + ""


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("sensor_data")


def on_message(client, userdata, msg):
    data = int(msg.payload)
    headers = {
        "Content-Type": "application/json",
        "Authorization": auth_token
    }
    # Automate the 'start' value so that for every day, it starts from 00:00
    now = datetime.datetime.now()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    start = start.isoformat() + "+01:00"
    payload = {
        "sensor": "ea1.2023-03.localhost:fm1.2",
        "values": [data],
        "duration": "PT24H",
        "start": start,
        "unit": "MW"
    }
    url = "http://localhost:5000/api/v3_0/sensors/data"
    response = requests.post(url, headers=headers, json=payload)
    print(response.json())


client = mqtt.Client()
client.connect("broker.mqttdashboard.com", 1883, 60)

client.on_connect = on_connect
client.on_message = on_message

try:
    client.loop_forever()
except KeyboardInterrupt:
    client.disconnect()
    print("Connection closed")
except Exception as e:
    print("Error: ", e)
