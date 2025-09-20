#include <Arduino.h>

// put function declarations here:
// int myFunction(int, int);

const int WIO_LIGHT = A0; // the number of the GPIO pin connected to the on-board light sensor.

void setup()
{
  // put your setup code here, to run once:
  // int result = myFunction(2, 3);
  Serial.begin(9600);
  while (!Serial)
    ;
  delay(1000);

  // configures the pins used to communicate with the sensor hardware
  // set to INPUT meaning it connects to a sensor and data will be read from the pin
  pinMode(WIO_LIGHT, INPUT);
}

void loop()
{
  // put your main code here, to run repeatedly:
  // Serial.println("Hello, World!");
  // delay(5000);

  // reads an analog value(from 0-1,023) from the WIO_LIGHT pin for the on-board light sensor
  // This analog value is then sent to the serial port so you can read it in the Serial Monitor when the code is running.
  int light = analogRead(WIO_LIGHT);
  Serial.print("Light value: ");
  Serial.println(light);

  // a small delay of one second (1,000ms) at the end of the loop since the light levels don't need to be checked continuously
  // This delay reduces the power consumption of the device
  delay(1000);
}

// put function definitions here:
// int myFunction(int x, int y) {
//   return x + y;
// }