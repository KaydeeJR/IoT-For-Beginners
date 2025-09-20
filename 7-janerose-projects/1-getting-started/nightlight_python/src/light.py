import logging
import time
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
from counterfit_connection import CounterFitConnection

logging.basicConfig(level=logging.INFO)

try:
    # Initialize connection with error handling
    CounterFitConnection.init("127.0.0.1", 5000)
    logging.info("Connected to CounterFit server")
    # connect to pin 0 - the CounterFit Grove pin that the light sensor is connected to.
    light_sensor = GroveLightSensor(pin=0)

    while True:
        # poll the light sensor value and print it to the console
        # the light property of the GroveLightSensor class reads the analog value from the pin
        light = light_sensor.light
        print('Light level:', light)
        # no need to check for light levels continuously, wait for a second before polling again
        # this reduces the power consumption of the device
        time.sleep(1)

except ConnectionError as e:
    logging.error(f"Connection error: {e}")
    logging.error("Make sure CounterFit server is running by typing: Counterfit in the terminal.")