import os
import subprocess
import sys
import signal
import CameraStreamer
import time

IMAGE_NAME = "/home/pi/Pictures/telegram_request.jpg"

subprocessVideo = None



class ChatMessager:
    def __init__(self) -> None:
        self.cameraStreamer = CameraStreamer.CameraStreamer()

    ####################################
    # Received Message Handlers        #
    ####################################

    def handle_message_unknown(self, update):
        print("Unsupported command")
        update.message.reply_text("Unsuported command, " +
        "type help to get all available commands")

    def handle_message_help(self, update):
        update.message.reply_text("Available commands:\n" +
        "\"exit\" \t\t Shut down the bot\n"
        "\"temp\" \t\t Get temperature of the room\n"
        "\"photo\" \t\t Get photo\n"
        "\"video start\" \t\t Start video stream\n"
        "\"video stop\" \t\t Stop video stream\n"
        )

    def handle_message_exit(self, update):
        update.message.reply_text("Bot turning off...")
        exit()

    def handle_message_temp(self, update):   
        try:
            rsp = str(subprocess.check_output("vcgencmd measure_temp", shell=True))
            import re
            val = re.findall("\d+\.\d+", rsp)[0]
            update.message.reply_text("Temperature of the RPi: " + str(val) + " C")
        except:
            update.message.reply_text("ERROR: Get temperature of the RPi")

    def handle_message_photo(self, update):
        update.message.reply_text("Taking photo...")
        if os.system("raspistill -o " + IMAGE_NAME) != 0: # -vf flag for flip
            update.message.reply_text("Camera Unavailable")
            return
        update.message.reply_text("Sending the photo...")
        f = open(IMAGE_NAME, "rb")
        update.message.reply_photo(f)

    def handle_message_videoStart(self, update):
        self.cameraStreamer.start()
        try:
            videoUrl = self.cameraStreamer.get_url()
            update.message.reply_text("url: "+ videoUrl)
        except:
            update.message.reply_text("ERROR: Failed to get my IP address")


    def handle_message_videoStop(self, update):
        self.cameraStreamer.stop()
        update.message.reply_text("Video streaming stopped")


    def received_message_handlers(self, message):
        """
        Return corresponding handler based on the message
        """
        switcher = {
            "help":             self.handle_message_help,
            "exit":             self.handle_message_exit,
            "temp":             self.handle_message_temp,
            "photo":            self.handle_message_photo,
            "video start":      self.handle_message_videoStart,
            "video stop":       self.handle_message_videoStop,
        }
        return switcher.get(message, self.handle_message_unknown)

    def handle_received_message(self, update):
        """
        Call Corresponding handler for the received message
        """
        self.received_message_handlers(update.message.text)(update)


