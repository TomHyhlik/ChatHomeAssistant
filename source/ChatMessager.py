import os
import subprocess
import sys
import signal
import CameraStreamer
import time

IMAGE_NAME = "/home/pi/Pictures/telegram_request.jpg"

subprocessVideo = None



def init():
    cameraStreamer = CameraStreamer.CameraStreamer()


####################################
# Received Message Handlers        #
####################################

def Handle_Received_Unknown(update):
    print("Unsupported command")
    update.message.reply_text("Unsuported command, " +
    "type help to get all available commands")



def Handle_Received_Help(update):
    update.message.reply_text("Available commands:\n" +
    "\"exit\" \t\t Shut down the bot\n"
    "\"temp\" \t\t Get temperature of the room\n"
    "\"photo\" \t\t Get photo\n"
    "\"video start\" \t\t Start video stream\n"
    "\"video stop\" \t\t Stop video stream\n"
    )



def Handle_Received_Exit(update):
    update.message.reply_text("Bot turning off...")
    exit()



def Handle_Received_Temp(update):   
    try:
        rsp = str(subprocess.check_output("vcgencmd measure_temp", shell=True))
        import re
        val = re.findall("\d+\.\d+", rsp)[0]
        update.message.reply_text("Temperature of the RPi: " + str(val) + " C")
    except:
        update.message.reply_text("ERROR: Get temperature of the RPi")





def Handle_Received_Photo(update):
    update.message.reply_text("Taking photo...")
    if os.system("raspistill -o " + IMAGE_NAME) != 0: # -vf flag for flip
        update.message.reply_text("Camera Unavailable")
        return
    update.message.reply_text("Sending the photo...")
    f = open(IMAGE_NAME, "rb")
    update.message.reply_photo(f)




def Handle_Received_VideoStart(update):
    cameraStreamer.start()
    try:
        videoUrl = cameraStreamer.GetUrl()
        update.message.reply_text("url: "+ videoUrl)
    except:
        update.message.reply_text("ERROR: Failed to get my IP address")




def Handle_Received_VideoStop(update):
    cameraStreamer.Stop()



def ReceivedMessageHandler(message):
    """
    Return corresponding handler based on the message
    """
    switcher = {
        "help":             Handle_Received_Help,
        "exit":             Handle_Received_Exit,
        "temp":             Handle_Received_Temp,
        "photo":            Handle_Received_Photo,
        "video start":      Handle_Received_VideoStart,
        "video stop":       Handle_Received_VideoStop,
    }
    return switcher.get(message, Handle_Received_Unknown)


    
def HandleReceived(update):
    """
    Call Corresponding handler for the received message
    """
    ReceivedMessageHandler(update.message.text)(update)


