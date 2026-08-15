# Code uses virtual CounterFit hardware to simulate a temperature, humidity,
# soil moisture and relay devices
from os import path

import csv
from datetime import datetime
import logging
import json
import time

from counterfit_shims_seeed_python_dht import DHT
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay

from counterfit_connection import CounterFitConnection
# this library automatically checks if there is a network connection
from paho.mqtt import client as mqtt_client

logging.basicConfig(level=logging.INFO)

CLIENT_ID = "2fe8f0bf6f440b14087f4b66ae305e13bd5b1b5d39480a8995be1834abf3ff46"

CLIENT_TELEMETRY_TOPIC = CLIENT_ID + r"/telemetry"
SERVER_COMMAND_TOPIC = CLIENT_ID + r"/command"

CLIENT_NAME = CLIENT_ID + r"/nightlight_server"
BROKER_URL = "test.mosquitto.org"

mqtt_client = mqtt_client.Client(callback_api_version=2, client_id=CLIENT_NAME)
mqtt_client.connect(BROKER_URL)

mqtt_client.loop_start()

base_dir = path.abspath(path.join(path.dirname(__file__), ".."))
docs_dir = path.join(base_dir, "docs")
temperature_file_name = path.join(docs_dir, "temperature.csv")

fieldnames = ['datetime', 'temperature']

if not path.exists(temperature_file_name):
    with open(temperature_file_name, mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()


def handle_command(payload):
    # device-side: handle incoming command messages (RelayOn) from the server
    relay_val = bool(payload.get("RelayOn", False))
    logging.info("Applying command RelayOn = %s", relay_val)
    try:
        if relay_val:
            relay.on()
        else:
            relay.off()
    except Exception as e:
        logging.error("Failed to set relay state: %s", e)


def process_telemetry(payload):
    """
    Process telemetry data locally and control relay based on moisture levels
    """
    try:
        temperature = int(payload.get("temperature", -1))
        humidity = int(payload.get("humidity", -1))
        soil_moisture = int(payload.get("moisture", -1))
        if soil_moisture < 45:
            print(
                f"Soil Moisture is {soil_moisture}% - too low, turning relay ON.")
            relay.on()
            relay_state = True
        else:
            print(
                f"Soil Moisture is {soil_moisture}% - sufficient, turning relay OFF.")
            relay.off()
            relay_state = False
        command = {"relay_on": relay_state}
        command_payload = json.dumps(command)
        logging.info("Publishing local command: %s", command_payload)
        mqtt_client.publish(SERVER_COMMAND_TOPIC, command_payload)
        # store temperature values to CSV file
        with open(temperature_file_name, mode='a') as temperature_file:
            temperature_writer = csv.DictWriter(
                temperature_file, fieldnames=fieldnames)
            # The data is stored in ISO 8601 format with the timezone, but without microseconds.
            temperature_writer.writerow({'datetime': datetime.now().astimezone().replace(
                microsecond=0).isoformat(), 'temperature': payload['temperature']})
    except Exception as e:
        logging.error("Invalid telemetry payload: %s", e)
        return
    logging.info("Processing telemetry temperature = %d °C | humidity = %d %%", temperature, humidity)


def on_message_handler(client, userdata, message):
    """
    Handle incoming MQTT messages (for external commands only)
    """
    try:
        payload = json.loads(message.payload.decode())
    except Exception as e:
        logging.error("Invalid JSON: %s", e)
        return

    logging.info("Received on %s: %s", message.topic, payload)
    if message.topic == SERVER_COMMAND_TOPIC:
        handle_command(payload)
    else:
        logging.warning("Unhandled topic: %s", message.topic)


# set handler and subscribe to both telemetry and command topics
mqtt_client.on_message = on_message_handler

mqtt_client.subscribe(CLIENT_TELEMETRY_TOPIC)
mqtt_client.subscribe(SERVER_COMMAND_TOPIC)

try:
    CounterFitConnection.init("127.0.0.1", 5000)
    logging.info("Connected to CounterFit server")
    # dht type is a virtual Digital Humidity and Temperature (DHT11) sensor
    dht_sensor = DHT(dht_type="11", pin=5)
    adc_sensor = ADC()
    relay = GroveRelay(pin=15)

    while True:
        # poll the temperature sensor value
        try:
            humidity, temp = dht_sensor.read()
            soil_moisture = adc_sensor.read(0)

            logging.info('Temperature: %d  °C | Humidity: %d %% | Soil Moisture: %d %%', int(
            temp), int(humidity), int(soil_moisture))

            telemetry = {
                "temperature": int(temp),
                "humidity": int(humidity),
                "moisture": int(soil_moisture),
                "timestamp": int(time.time() * 1000)
            }
            process_telemetry(telemetry)
            payload = json.dumps(telemetry)
            logging.info("Publishing telemetry: %s", payload)
            mqtt_client.publish(CLIENT_TELEMETRY_TOPIC, payload)

            # no need to check the sensor values continuously
            # wait for a second before polling again
            # this reduces the power consumption of the device
            time.sleep(10)
        except Exception as e:
            logging.exception(
                "Failed to read DHT sensor (check CounterFit server & sensor pin).")
            # in case of error then wait and retry instead of crashing
            time.sleep(10)
            continue

except ConnectionError as e:
    logging.error(f"Connection error: {e}")
    logging.error(
        "Make sure CounterFit server is running by typing: `Counterfit` in the terminal.")
