# Code uses virtual CounterFit hardware to simulate a nightlight device
# that turns on an LED when values are below a threshold and turns it off when above.
import logging
import json
import time

from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
from counterfit_shims_grove.grove_led import GroveLed

from counterfit_connection import CounterFitConnection
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


def handle_command(payload):
    # device-side: handle incoming command messages (LedOn) from the server
    led_val = bool(payload.get("LedOn", False))
    logging.info("Applying command LedOn = %s", led_val)
    try:
        if led_val:
            led.on()
        else:
            led.off()
    except Exception as e:
        logging.error("Failed to set led state: %s", e)


def process_telemetry(payload):
    """
    Simple controller logic:
    - Expect payload like {"lightIn": <int>, "timestamp": ...}
    - Decide LedOn based on LIGHT_THRESHOLD and publish to SERVER_COMMAND_TOPIC.
    """
    try:
        light_in = int(payload.get("lightIn", -1))
    except Exception as e:
        logging.error("Invalid telemetry payload: %s", e)
        return
    logging.info("Processing telemetry lightIn = %d", light_in)
    led_val = light_in < LIGHT_THRESHOLD
    command_to_run = {"LedOn": led_val}
    mqtt_client.publish(SERVER_COMMAND_TOPIC, json.dumps(command_to_run))
    logging.info("Published command: %s to topic %s",
                 command_to_run, SERVER_COMMAND_TOPIC)

    # if this process hosts the device (single-process test), apply immediately
    if 'led' in globals():
        try:
            handle_command(command_to_run)
        except Exception as e:
            logging.error("Failed to apply command locally: %s", e)


def on_message(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode())
    except Exception as e:
        logging.error("Invalid JSON: %s", e)
        return

    logging.info("Received on %s: %s", message.topic, payload)
    if message.topic == CLIENT_TELEMETRY_TOPIC:
        process_telemetry(payload)       # existing controller logic
    elif message.topic == SERVER_COMMAND_TOPIC:
        handle_command(payload)          # apply command to the led
    else:
        logging.warning("Unhandled topic: %s", message.topic)


# set handler and subscribe to both telemetry and command topics
mqtt_client.on_message = on_message
mqtt_client.subscribe(CLIENT_TELEMETRY_TOPIC)
mqtt_client.subscribe(SERVER_COMMAND_TOPIC)

try:
    CounterFitConnection.init("127.0.0.1", 5000)
    logging.info("Connected to CounterFit server")
    light_sensor = GroveLightSensor(pin=0)
    led = GroveLed(pin=5)

    while True:
        # poll the light sensor value - the light property of the GroveLightSensor class reads the analog value from the pin
        try:
            light = light_sensor.light
            logging.info('Light level (local): %d', int(light))
            telemetry = {
                "lightIn": int(light),
                "timestamp": int(time.time() * 1000)
            }
            payload = json.dumps(telemetry)
            logging.info("Publishing telemetry: %s", payload)
            mqtt_client.publish(CLIENT_TELEMETRY_TOPIC, payload)
            # no need to check for light levels continuously, wait for a second before polling again
            # this reduces the power consumption of the device
            time.sleep(2)
        except Exception as e:
            logging.exception(
                "Failed to read light sensor (check CounterFit server & sensor pin).")
            # in case of error then wait and retry instead of crashing
            time.sleep(5)
            continue

except ConnectionError as e:
    logging.error(f"Connection error: {e}")
    logging.error(
        "Make sure CounterFit server is running by typing: `Counterfit` in the terminal.")
