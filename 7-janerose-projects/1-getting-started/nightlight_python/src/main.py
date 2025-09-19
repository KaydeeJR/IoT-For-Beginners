from counterfit_connection import CounterFitConnection
import io
import time
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

try:
    # Initialize connection with error handling
    CounterFitConnection.init("127.0.0.1", 5000)
    logging.info("Connected to CounterFit server")
    
    # Add a small delay to ensure connection is established
    time.sleep(1)
    
    from counterfit_shims_picamera import PiCamera
    
    camera_device = PiCamera()
    camera_device.resolution = (640, 480)
    camera_device.rotation = 0
    
    logging.info("Camera initialized, capturing image...")
    
    camera_image = io.BytesIO()
    camera_device.capture(camera_image, image_format='png')
    camera_image.seek(0)
    
    # Create a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"camera_image_{timestamp}.png"
    
    with open(filename, "wb") as image_file:
        image_file.write(camera_image.read())
    
    logging.info(f"Image captured successfully: {filename}")
    
except ConnectionError as e:
    logging.error(f"Connection error: {e}")
    logging.error("Make sure CounterFit server is running by typing: Counterfit in the terminal.")
except Exception as e:
    logging.error(f"Error: {e}")
