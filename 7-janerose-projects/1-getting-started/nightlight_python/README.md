# Nightlight (Python)

A small, beginner-friendly Python project that demonstrates reading a light sensor and capturing images using a virtual PiCamera for IoT experimentation with CounterFit. This repository contains example code to connect to a CounterFit server, read a Grove light sensor, and capture images from a PiCamera sensor simulated by CounterFit.

Quick links
- Project folder: nightlight_python
- Example scripts: src/camera.py, src/app.py (light sensor)
- Screenshots: etc/

Overview
- Read simulated light sensor values (Grove Light Sensor shim).
- Capture and save images using the PiCamera shim or a webcam source provided by CounterFit.
- Intended for use with the CounterFit virtual device server (local web UI).

Prerequisites
- Python 3.13+ (or compatible 3.x)
- CounterFit server installed and running locally
- Optional: virtual environment for Python dependencies

Recommended dependencies
- counterfit
- counterfit-shims-grove
- counterfit-shims-picamera
- counterfit-shims-serial
- werkzeug==2.2.3 (compatibility note)

Quick start (local)
1. Create and activate a virtual environment (recommended)
   - Windows PowerShell:
     ```
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   - Windows cmd:
     ```
     python -m venv .venv
     .venv\Scripts\activate
     ```
2. Install dependencies:
   - If a requirements.txt file exists:
     ```
     pip install -r requirements.txt
     ```
   - Otherwise:
     ```
     pip install counterfit counterfit-shims-grove counterfit-shims-picamera counterfit-shims-serial werkzeug==2.2.3
     ```
3. Start CounterFit server:
   ```
   Counterfit
   ```
   Open [http://localhost:5000](http://localhost:5000) in a browser.
4. Create sensors in the CounterFit UI (see sections below).
5. Run scripts:
   - Camera capture:
     ```
     python "./src/camera.py"
     ```
   - Light sensor loop:
     ```
     python "./src/app.py"
     ```

Create and configure sensors in CounterFit
- Camera (PiCamera)
  1. In the CounterFit web UI → Sensors → Create sensor.
  2. Select Sensor type: Camera.
  3. Name: Picamera (or any name you prefer).
  4. Source: WebCam (or other available source).
  5. Click Add → Set.
  The camera sensor will appear in the sensor list and be available to scripts.

- Light (Grove Light Sensor)
  1. In the CounterFit web UI → Sensors → Create sensor.
  2. Select Sensor type: Light.
  3. Units: NoUnits (default).
  4. Pin: 0
  5. Click Add → Set.
  You can set a fixed Value or check Random and enter Min/Max to simulate changing light.

Example code snippets

- Minimal light sensor loop (src/app.py)
```python
# filepath: src/app.py
import time
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor

light_sensor = GroveLightSensor(0)

while True:
    light = light_sensor.light
    print('Light level:', light)
    time.sleep(1)
```

- Minimal camera capture (src/camera.py)
```python
# filepath: src/camera.py
from counterfit_shims_picamera.picamera import PiCamera
from datetime import datetime

camera = PiCamera()
filename = f"capture_{datetime.now():%Y%m%d_%H%M%S}.jpg"
camera.capture(filename)
print("Saved image to", filename)
```

File layout (important files)
- src/
  - app.py        — example light sensor loop (reads GroveLightSensor on pin 0)
  - camera.py     — example camera capture script
- etc/            — screenshots and supporting images
- requirements.txt — optional dependency list

Running and verifying
- Start CounterFit and create the sensors described above.
- Run src/camera.py to capture an image — check the project folder for saved images.
- Run src/app.py to start printing simulated light values to the console.
- In the CounterFit UI you can change the light sensor Value or enable Random to see changing outputs.

Troubleshooting
- If values stay at 0: ensure the light sensor is created and assigned to pin 0 in CounterFit.
- If camera capture fails: confirm Picamera sensor exists and Source is set to WebCam (or an available source).
- If you see werkzeug/Flask compatibility errors: try werkzeug==2.2.3 as noted above.
- Virtual environment: make sure the terminal session has the venv activated when running scripts.

Testing tips
- Use the Random option in CounterFit for the light sensor to simulate dynamic behavior.
- Capture multiple images with different camera settings (if available in your PiCamera shim).

Contributing
- Improvements and bug fixes welcome via pull requests or issues.
- Keep changes focused and provide a short description of why the change helps beginners.

License
- Add a LICENSE file in the project root or include license metadata here.

Contacts and references
- CounterFit project: https://github.com/counterfitio (refer to official docs for server usage)
- This project is designed for learning and simulation; do not use it in production environments without appropriate security and hardware validation.
