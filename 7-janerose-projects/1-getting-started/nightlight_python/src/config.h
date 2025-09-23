#pragma once

using namespace std;

// WiFi credentials to connect to the internet
char SSID[] = "Wokwi-GUEST";
char PASSWORD[] = "";

// MQTT settings
const String CLIENT_ID = "2fe8f0bf6f440b14087f4b66ae305e13bd5b1b5d39480a8995be1834abf3ff46"; // every device will need a unique ID to connect to the broker

const String BROKER_URL = "test.mosquitto.org";
const String CLIENT_NAME = CLIENT_ID + "nightlight_client";
const String CLIENT_TELEMETRY_TOPIC = CLIENT_ID + "/telemetry"; // topic to publish telemetry data to
const String SERVER_COMMAND_TOPIC = CLIENT_ID + "/command";     // topic to subscribe to for server commands
