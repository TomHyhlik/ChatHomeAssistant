"""
Test PIR Sensor handler
"""

import threading
import time
import PirHandler

GPIO_PIR = 16

def handle_pir_trigger():
    print("PIR Triggered")

# Setup PirHandler
pirHandler = PirHandler.PirHandler(GPIO_PIR)
pirHandler.register_callback(handle_pir_trigger)

# Run the PirHandler in thread so it is not blocking
thread = threading.Thread(target=pirHandler.start)
thread.start()

print("Test PIR handler initialized")

while True:
    time.sleep(1)