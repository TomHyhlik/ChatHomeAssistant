import os
import subprocess
import CameraStreamer

IMAGE_NAME = "/home/pi/Pictures/telegram_request.jpg"

LOG_NAME = "CHM "

subprocessVideo = None

class   ChatMessager:
    """
    Receive and handle messages from ChatCommunicator
    """
    def __init__(self, chatCommunicator) -> None:
        self.chatCommunicator = chatCommunicator
        self.chatCommunicator.register_callback_on_received_message(self.callback_on_received_message)
        self.cameraStreamer = CameraStreamer.CameraStreamer()

    def callback_on_received_message(self, handle, message):
        """
        Callback called on chat message received
        """
        self.received_message_handlers(message)(handle)

    ####################################
    # Received Message Handlers        #
    ####################################

    def handle_message_unknown(self, handle):
        print(LOG_NAME + "Unsupported command")
        self.chatCommunicator.send_reply_message_text(handle, "Unsuported command, " +
        "type help to get all available commands")

    def handle_message_help(self, handle):
        self.chatCommunicator.send_reply_message_text(handle, "Available commands:\n" +
        "\"exit\" \t\t Shut down the bot\n"
        "\"temp\" \t\t Get temperature of the room\n"
        "\"photo\" \t\t Get photo\n"
        "\"video start\" \t\t Start video stream\n"
        "\"video stop\" \t\t Stop video stream\n"
        )

    def handle_message_exit(self, handle):
        self.chatCommunicator.send_reply_message_text(handle, "Bot turning off...")
        exit()

    def handle_message_temp(self, handle):   
        try:
            rsp = str(subprocess.check_output("vcgencmd measure_temp", shell=True))
            import re
            val = re.findall("\d+\.\d+", rsp)[0]
            self.chatCommunicator.send_reply_message_text(handle, "Temperature of the RPi: " + str(val) + " C")
        except:
            self.chatCommunicator.send_reply_message_text(handle, "ERROR: Get temperature of the RPi")

    def handle_message_photo(self, handle):
        self.chatCommunicator.send_reply_message_text(handle, "Taking photo...")
        if os.system("raspistill -o " + IMAGE_NAME) != 0: # -vf flag for flip
            self.chatCommunicator.send_reply_message_text(handle, "Camera Unavailable")
            return
        self.chatCommunicator.send_reply_message_text(handle, "Sending the photo...")
        f = open(IMAGE_NAME, "rb")
        self.chatCommunicator.send_reply_message_photo(handle, f)

    def handle_message_videoStart(self, handle):
        self.cameraStreamer.start()
        try:
            videoUrl = self.cameraStreamer.get_url()
            self.chatCommunicator.send_reply_message_text(handle, "url: "+ videoUrl)
        except:
            self.chatCommunicator.send_reply_message_text(handle, "ERROR: Failed to get my IP address")


    def handle_message_videoStop(self, handle):
        self.cameraStreamer.stop()
        self.chatCommunicator.send_reply_message_text(handle, "Video streaming stopped")


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


