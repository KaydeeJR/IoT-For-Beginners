# Code for the server that receives and processes telemetry from the device, makes 
# and sends commands back to it based on light levels.
import logging
import json
import time

#  this library automatically checks if there is a network connection
from paho.mqtt import client as mqtt_client

logging.basicConfig(level=logging.INFO)

CLIENT_ID = "2fe8f0bf6f440b14087f4b66ae305e13bd5b1b5d39480a8995be1834abf3ff46"

CLIENT_TELEMETRY_TOPIC = CLIENT_ID + r"/telemetry"
SERVER_COMMAND_TOPIC = CLIENT_ID + r"/command"

CLIENT_NAME = CLIENT_ID + r"/nightlight_server"
BROKER_URL = "test.mosquitto.org"

LIGHT_THRESHOLD = 300

mqtt_client = mqtt_client.Client(callback_api_version=2, client_id=CLIENT_NAME)
mqtt_client.connect(BROKER_URL)

mqtt_client.loop_start()


def receive_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    logging.info("Received telemetry on topic: %s", message.topic)
    process_telemetry(payload)


def process_telemetry(payload):
    logging.info("Processing telemetry...")
    INVERT_LOGIC = False  # Lower lux values = darker = LED on
    light_val = int(payload.get('lightIn', 0))
    logging.info("lightIn = %d, threshold = %d, invert = %s", light_val, LIGHT_THRESHOLD, INVERT_LOGIC)

    led_on = light_val < LIGHT_THRESHOLD  # Lower light = LED on
    
    command = {'LedOn': led_on}
    mqtt_client.publish(SERVER_COMMAND_TOPIC, json.dumps(command))
    logging.info("Sent command: %s", command)


mqtt_client.on_message = receive_telemetry
mqtt_client.subscribe(CLIENT_TELEMETRY_TOPIC)

while True:
    time.sleep(2)
