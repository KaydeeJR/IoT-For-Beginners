# Nightlight (Python)

A simple Python-based nightlight project for small IoT experiments. This repository contains code to connect to counterfit server and capture images via a PiCamera sensor.

## Features
- Captures an image and saves the image to file.

## Prerequisites
- Python 3.13+

## Installation

1. Create and activate a virtual environment (recommended):
   - Windows:
     ```
     python -m venv .venv
     source "./.venv/Scripts/activate"
     ```

2. Install dependencies (if a requirements.txt exists):
   ```
   pip install -r requirements.txt
   ```
   If no requirements file is present, install hardware libraries as needed:
   ```
   pip install counterfit counterfit-shims-grove counterfit-shims-serial counterfit-shims-picamera werkzeug==2.2.3
   ```

## Run
Start the Counterfit server:

```
Counterfit
```

Open http://127.0.0.1:5000/ in a browser.

Create a Camera Sensor:
- Sensor Type: Camera
- Name: Picamera

Click Add

Configure Source: WebCam

Click Set

Run the main script:

```
python "./src/main.py"
```

## Project Structure (example)
- src/main.py        - main entrypoint
- requirements.txt     - Python dependencies

## Contributing
- Open an issue or pull request with improvements.

## License
Add a LICENSE file or include license details here.

