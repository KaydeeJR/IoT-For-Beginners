# Code uses virtual CounterFit hardware to simulate a nightlight device
# that turns on an LED when it is dark and turns it off when it is bright.

# Virtual LED does not turn on even though the command is received from the server - {'LedOn': True}.
import logging
import json
import time

from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
from counterfit_shims_grove.grove_led import GroveLed

from counterfit_connection import CounterFitConnection

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

# device-side: handle incoming command messages (LedOn) from the server


def receive_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Received telemetry on topic:", message.topic)
    process_telemetry(payload)


def process_telemetry(payload):
    print("Processing telemetry...")
    INVERT = False
    light_val = int(payload.get('lightIn', 0))
    print("lightIn =", light_val, "threshold =",
          LIGHT_THRESHOLD, "invert =", INVERT)
    if INVERT:
        led_on = light_val > LIGHT_THRESHOLD
    else:
        led_on = light_val < LIGHT_THRESHOLD
    command = {'LedOn': led_on}
    mqtt_client.publish(SERVER_COMMAND_TOPIC, json.dumps(command))
    print("Sent command:", command)


# set handler before subscribing
mqtt_client.on_message = receive_telemetry
mqtt_client.subscribe(CLIENT_TELEMETRY_TOPIC)

try:
    # Initialize connection with error handling
    CounterFitConnection.init("127.0.0.1", 5000)
    logging.info("Connected to CounterFit server")
    # connect to pin 0 - the CounterFit Grove pin that the light sensor is connected to.
    light_sensor = GroveLightSensor(pin=0)
    led = GroveLed(pin=5)

    while True:
        # poll the light sensor value and print it to the console
        # the light property of the GroveLightSensor class reads the analog value from the pin
        light = light_sensor.light
        print('Light level (local):', light)
        telemetry = {
            "lightIn": int(light),
            "timestamp": int(time.time() * 1000)
        }
        payload = json.dumps(telemetry)
        print("Publishing telemetry:", payload)
        mqtt_client.publish(CLIENT_TELEMETRY_TOPIC, payload)
        # no need to check for light levels continuously, wait for a second before polling again
        # this reduces the power consumption of the device
        time.sleep(2)

except ConnectionError as e:
    logging.error(f"Connection error: {e}")
    logging.error(
        "Make sure CounterFit server is running by typing: Counterfit in the terminal.")
