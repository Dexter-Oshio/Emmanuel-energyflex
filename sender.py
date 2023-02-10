import requests
import random
import time
import paho.mqtt.client as mqtt

# Set Mosquitto (MQTT) parameters
broker_address = "broker.emqx.io"
port = 1883
topic = "sensor_data"


# Create a function to publish simulated sensor data
def publish_data():
    # Generate simulated sensor data
    data = str(random.randint(0, 100))
    print("Publishing data: ", data)


# Create a MQTT client
client = mqtt.Client()

# Connect to the MQTT broker
client.connect(broker_address, port)

# Publish sensor data every 5 seconds
try:
    while True:
        publish_data()
        time.sleep(5)

# Handle any exceptions that may occur
except KeyboardInterrupt:
    print("Connection closed")

except Exception as e:
    print("Error: ", e)

finally:
    client.disconnect()
