# Getting Started — Janerose IoT Projects

Pick a path below and follow the README in that folder for full step‑by‑step instructions.

Paths:
The Arduino path uses PlatformIO for building and uploading code, and Wokwi for simulation.
- Arduino — microcontroller path (PlatformIO + Wokwi)
  - Folder: [nightlight_arduino/](./nightlight_arduino/)  
  - Focus: build firmware, read light values from an LDR sensor, run in Wokwi or on a physical Arduino.

The Python path uses CounterFit/Wokwi for virtual devices and MQTT for messaging.
- Python — virtual devices path (CounterFit/Wokwi + MQTT)  
  - Folder: [nightlight_python/](./nightlight_python/)
    - The Python path has 2 separate telemetry projects:
      - `nightlight.py`: simulates telemetry and commands using CounterFit (python library).
      - `nightlight_server.py`: simulates telemetry and commands using wokwi, Python and PlatformIO.
  - Focus: simulated sensors/actuators, PiCamera capture, publish/subscribe telemetry via MQTT.

How to use:
1. Choose a path above.
2. Open the matching folder and follow that folder's README for prerequisites, exact commands, wiring, and troubleshooting.

Structure:
- nightlight_arduino/ — Arduino sketch, wokwi config, diagram, PlatformIO project
- nightlight_python/ — Python scripts, Python packages, requirements.txt, wokwi config, diagram, PlatformIO project

Notes
- Each subfolder README contains full detail; this index is intentionally minimal.
