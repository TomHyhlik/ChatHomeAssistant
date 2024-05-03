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

def handle_cmd_help(update):
    update.message.reply_text("Available commands:\n" +
    "\"exit\" \t\t Shut down the bot\n"
    "\"temp\" \t\t Get temperature of the room\n"
    "\"temp rpi\" \t\t Get temperature of the device\n"
    "\"humid\" \t\t Get hummidity\n"
    "\"photo\" \t\t Get photo\n"
    )

def handle_cmd_exit(update):
    update.message.reply_text("Bot turning off...")
    sys.exit()

def handle_cmd_temp(update):
    update.message.reply_text("Temperature in the room: 22.84 C")

def handle_cmd_tempRpi(update):   
    try:
        rsp = str(subprocess.check_output("vcgencmd measure_temp", shell=True))
        import re
        val = re.findall("\d+\.\d+", rsp)[0]
        update.message.reply_text("Temperature of the RPi: " + str(val) + " C")
    except:
        update.message.reply_text("ERROR: Get temperature of the RPi")

def handle_cmd_humidity(update):
    update.message.reply_text("TODO: To be added")

def handle_cmd_photo(update):
    update.message.reply_text("Taking photo...")
    if os.system("raspistill -o " + IMAGE_NAME) != 0: # -vf flag for flip
        update.message.reply_text("Camera Unavailable")
        return
    update.message.reply_text("Sending the photo...")
    f = open(IMAGE_NAME, "rb")
    update.message.reply_photo(f)

def handle_cmd_video_start(update):
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

def handle_cmd_video_stop(update):
    global proc_videoStream
    if proc_videoStream == None:
        update.message.reply_text("Video streaming is not running")
    else:
        update.message.reply_text("Video streaming stopped")     
        proc_videoStream.terminate()
        proc_videoStream = None


################################ Handle Cmd
def handleCmd(argument):
    switcher = {
        "help":             handle_cmd_help,
        "exit":             handle_cmd_exit,
        "temp":             handle_cmd_temp,
        "temp rpi":         handle_cmd_tempRpi,
        "humid":            handle_cmd_humidity,
        "photo":            handle_cmd_photo,
        "video start":      handle_cmd_video_start,
        "video stop":       handle_cmd_video_stop,
    }
    return switcher.get(argument, handle_cmd_unknown)


    
def HandleReceived(update):
    handleCmd(update.message.text)(update)

