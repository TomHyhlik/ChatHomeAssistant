import os
import subprocess
import sys

import time

IMAGE_NAME = "/home/pi/Pictures/telegram_request.jpg"

proc_videoStream = None

################################ Cmd handlers

def handle_cmd_unknown(update):
    print("Unsupported command")
    update.message.reply_text("Unsuported command, " +
    "type help to get all available commands")

def Handle_Received_Help(update):
    update.message.reply_text("Available commands:\n" +
    "\"exit\" \t\t Shut down the bot\n"
    "\"temp\" \t\t Get temperature of the room\n"
    "\"temp rpi\" \t\t Get temperature of the device\n"
    "\"humid\" \t\t Get hummidity\n"
    "\"photo\" \t\t Get photo\n"
    )

def Handle_Received_Exit(update):
    update.message.reply_text("Bot turning off...")
    sys.exit()

def Handle_Received_Temp(update):
    update.message.reply_text("Temperature in the room: 22.84 C")

def Handle_Received_TempRpi(update):   
    try:
        rsp = str(subprocess.check_output("vcgencmd measure_temp", shell=True))
        import re
        val = re.findall("\d+\.\d+", rsp)[0]
        update.message.reply_text("Temperature of the RPi: " + str(val) + " C")
    except:
        update.message.reply_text("ERROR: Get temperature of the RPi")

def Handle_Received_Humid(update):
    update.message.reply_text("TODO: To be added")

def Handle_Received_Photo(update):
    update.message.reply_text("Taking photo...")
    if os.system("raspistill -o " + IMAGE_NAME) != 0: # -vf flag for flip
        update.message.reply_text("Camera Unavailable")
        return
    update.message.reply_text("Sending the photo...")
    f = open(IMAGE_NAME, "rb")
    update.message.reply_photo(f)

def Handle_Received_VideoStart(update):
    global proc_videoStream
    update.message.reply_text("Starting video streaming...")
    proc_videoStream = subprocess.Popen("python3 camera_surveillance_system.py &", shell=True)
    # Get access link
    try:
        myIpAddr = str(subprocess.check_output("hostname -I", shell=True))
        myIpAddr = myIpAddr[2:]
        myIpAddr = myIpAddr[:-4]
    except:
        update.message.reply_text("ERROR: Failed to get my IP address")
        return
    link = "Link: http://"+ str(myIpAddr) +":8000/"
    print("link: " + link)
    update.message.reply_text(link)

def Handle_Received_VideoStop(update):
    global proc_videoStream
    if proc_videoStream == None:
        update.message.reply_text("Video streaming is not running")
    else:
        update.message.reply_text("Video streaming stopped")     
        proc_videoStream.terminate()
        proc_videoStream = None



def ReceivedMessageHandler(message):
    """
    Return corresponding handler based on the message
    """
    switcher = {
        "help":             Handle_Received_Help,
        "exit":             Handle_Received_Exit,
        "temp":             Handle_Received_Temp,
        "temp rpi":         Handle_Received_TempRpi,
        "humid":            Handle_Received_Humid,
        "photo":            Handle_Received_Photo,
        "video start":      Handle_Received_VideoStart,
        "video stop":       Handle_Received_VideoStop,
    }
    return switcher.get(message, handle_cmd_unknown)


    
def HandleReceived(update):
    """
    Call Corresponding handler for the received message
    """
    ReceivedMessageHandler(update.message.text)(update)

