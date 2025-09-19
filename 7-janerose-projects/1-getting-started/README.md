# Getting Started — Janerose IoT Projects

## Overview
This folder contains beginner-friendly, hands-on IoT projects to help you get started with microcontrollers (Arduino) and simple sensors/actuators. Each project demonstrates basic setup, sample code, and steps to flash and run the code.

## Contents
- Example source code (see the repo's src/ folder)

## Prerequisites
- Basic familiarity with a microcontroller platform such as PlatformIO
- A USB cable and a PC running Windows OS
- Installed toolchain:
  - PlatformIO as a VS Code extension 
  - Python 3.13
  - pip
  - [counterfit](https://pypi.org/project/CounterFit/)

## Hardware
These projects make use of virtual IoT hardware components powered by CounterFit.

- (Optional) 1× microcontroller board: ATmega328 [Arduino Nano 3.x](https://docs.arduino.cc/hardware/nano/)

## Setup and Flashing an Arduino Nano
1. Click the PlatformIO icon on the left activity toolbar (the icon resembles an ant or an alien)
2. Click Pick a Folder then navigate to the appropriate project folder (the folder should be appended with `_arduino`)
3. Once the folder is open, navigate to the `src/main.cpp` file.
4. Click Build in the Left Activity Bar or on the bottom left PlatformIO toolbar.
5. Click Upload to flash the board.
6. Click Monitor to view the output.

## Running and Verifying
- After flashing, open the Serial Monitor to view logs or sensor readings.
- Verify LED blinks or sensor values update as expected.

## Troubleshooting
- If the board is not detected then check your cable.
- If you encounter compilation errors then ensure that you have the correct board type and that necessary libraries are installed.

## Where to look in this repo
- /src — source code and scripts
- /etc — Pinout diagrams, images (if present)
- README files provide detailed information about each subproject

## Resources
- Arduino getting started: https://docs.arduino.cc/
- ESP documentation: https://www.espressif.com/en/support/documents/technical-documents
- PlatformIO: https://platformio.org/

## License
Check the LICENSE file in the repository root for licensing details.