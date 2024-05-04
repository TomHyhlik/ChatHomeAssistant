"""
PIR Sensor handler
"""

import time
import RPi.GPIO as GPIO


class PirHandler:
    def __init__(self, gpio_pir):
        self.pir_triggered_callback = None
        self.pirGpio = gpio_pir


    def register_callback(self, callback):
        self.pir_triggered_callback = callback


    def start(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pirGpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        pirSamples = [False, False]

        while True:
            pirSamples[0] = pirSamples[1]
            pirSamples[1] = GPIO.input(self.pirGpio)
            if not pirSamples[0] and pirSamples[1]:
                self.pir_triggered_callback()
                time.sleep(5)
            time.sleep(.1)


