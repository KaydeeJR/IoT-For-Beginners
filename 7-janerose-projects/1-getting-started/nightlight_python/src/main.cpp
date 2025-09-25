// Runs on an ESP32-C3-DevKitC-02 board, reads a light sensor value, sends telemetry to an MQTT broker,
// and receives commands to control an external LED based on the telemetry data.
#include <Arduino.h>
#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <WiFi.h>

#include "config.h"

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

const int LIGHT_SENSOR_PIN = 2; // GPIO pin for light sensor
const int LED_PIN = 13;         // external LED wired to GPIO13 (series resistor to GND)

// put function declarations here:
void connectMqttClient();
void clientCallback(char *topic, uint8_t *payload, unsigned int length);

void connectWiFi()
{
  Serial.print("Connecting to WiFi SSID: ");
  Serial.println(SSID);

  WiFi.begin(SSID, PASSWORD);

  unsigned long start = millis();
  const unsigned long timeout = 20000; // 20s timeout

  while (WiFi.status() != WL_CONNECTED && (millis() - start) < timeout)
  {
    Serial.print(".");
    delay(500);
  }

  if (WiFi.status() == WL_CONNECTED)
  {
    Serial.println();
    Serial.print("Connected! IP address: ");
    Serial.println(WiFi.localIP());
  }
  else
  {
    Serial.println();
    Serial.print("Failed to connect, status=");
    Serial.println(WiFi.status());
    // ESP32 WiFi status codes:
    // 0 = WL_IDLE_STATUS, 1 = WL_NO_SSID_AVAIL, 3 = WL_CONNECTED,
    // 4 = WL_CONNECT_FAILED, 6 = WL_DISCONNECTED
  }
}

void createMqttClient()
{
  mqttClient.setServer(BROKER_URL.c_str(), 1883);
  connectMqttClient();
  // Call the callback function whenever incoming messages are received
  mqttClient.setCallback(clientCallback);
}

void setup()
{
  Serial.begin(115200); // ESP32 typically uses 115200 baud rate
  while (!Serial)
    ;
  delay(1000);

  // Configure pins
  pinMode(LIGHT_SENSOR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);

  // Initialize WiFi mode
  WiFi.mode(WIFI_STA);

  connectWiFi();
  createMqttClient();
}

void connectMqttClient()
{
  // recursively checks the connection to the MQTT broker and reconnects if the connection is lost
  while (!mqttClient.connected())
  {
    Serial.print("Attempting MQTT connection...");
    if (mqttClient.connect(CLIENT_NAME.c_str()))
    {
      Serial.println("connected");
      mqttClient.subscribe(SERVER_COMMAND_TOPIC.c_str());
      Serial.print("Subscribed to: ");
      Serial.println(SERVER_COMMAND_TOPIC);
    }
    else
    {
      Serial.print("failed, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void clientCallback(char *topic, uint8_t *payload, unsigned int length)
{
  // Convert payload to string
  char buff[length + 1];
  for (unsigned int i = 0; i < length; i++)
    buff[i] = (char)payload[i];
  buff[length] = '\0';

  Serial.print("Message arrived: ");
  Serial.println(buff);

  DynamicJsonDocument doc(1024);
  DeserializationError error = deserializeJson(doc, buff);
  if (error)
  {
    Serial.print("JSON parse failed: ");
    Serial.println(error.c_str());
    return;
  }

  JsonObject obj = doc.as<JsonObject>();
  bool LedOn = obj["LedOn"];

  Serial.print("Command received - LedOn: ");
  Serial.println(LedOn ? "TRUE" : "FALSE");

  if (LedOn)
  {
    digitalWrite(LED_PIN, HIGH); // turn the LED on
    Serial.println("LED turned ON");
  }
  else
  {
    digitalWrite(LED_PIN, LOW); // turn the LED off
    Serial.println("LED turned OFF");
  }
}

void loop()
{
  // Maintain MQTT connection
  if (!mqttClient.connected())
  {
    connectMqttClient();
  }
  mqttClient.loop();

  // Check WiFi connection
  if (WiFi.status() != WL_CONNECTED)
  {
    Serial.println("WiFi disconnected, reconnecting...");
    connectWiFi();
  }

  // Read light sensor value
  int lightIn = analogRead(LIGHT_SENSOR_PIN);
  Serial.print("Light value (local): ");
  Serial.println(lightIn);

  // Create and send telemetry
  DynamicJsonDocument doc(1024);
  doc["lightIn"] = lightIn;
  doc["timestamp"] = millis();

  String telemetry;
  serializeJson(doc, telemetry);

  Serial.print("Sending telemetry: ");
  Serial.println(telemetry);

  mqttClient.publish(CLIENT_TELEMETRY_TOPIC.c_str(), telemetry.c_str());

  delay(2000);
}