import random
import time
import paho.mqtt.client as mqtt

# Set Mosquitto (MQTT) parameters
broker_address = "broker.mqttdashboard.com"
port = 1883
topic = "iot/data"


# Create a function to publish simulated sensor data
def publish_data():
    # Generate simulated sensor data
    data = str(random.randint(100, 350))
    client.publish(topic, data)
    print("Data published:", data)

# Create a MQTT client
client = mqtt.Client()

# Connect to the MQTT broker
client.connect(broker_address, port)

# Publish sensor data every hour
try:
    for i in range(24):
        publish_data()
        time.sleep(60 * 60)  # sleep for one hour

# Handle exceptions that may occur
except KeyboardInterrupt:
    print("Connection closed")

except Exception as e:
    print("Error: ", e)

finally:
    client.disconnect()
