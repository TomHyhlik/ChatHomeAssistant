import os
import subprocess
import sys

import signal


IMAGE_NAME = "/home/pi/Pictures/telegram_request.jpg"

subprocessVideo = None



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
    "\"temp rpi\" \t\t Get temperature of the device\n"
    "\"humid\" \t\t Get hummidity\n"
    "\"photo\" \t\t Get photo\n"
    "\"video start\" \t\t Start video stream\n"
    "\"video stop\" \t\t Stop video stream\n"
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
    global subprocessVideo
    update.message.reply_text("Starting video streaming...")
    subprocessVideo = subprocess.Popen("python3 CameraStreamer.py", shell=True)
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


    # Kill the subprocess
    subprocessVideo.send_signal(signal.SIGINT)  # Sends the interrupt signal (Ctrl+C)
    # If the process does not terminate, force kill it
    if subprocessVideo.poll() is None:  # Check if the process is still running
        subprocessVideo.kill()  # Force kill the process
    # Wait for the process to terminate and get the exit code
    exit_code = subprocessVideo.wait()
    print(f"Process exited with code {exit_code}")






def Handle_Received_VideoStop(update):
    global subprocessVideo
    if subprocessVideo == None:
        update.message.reply_text("Video streaming is not running")
    else:
        # Kill the subprocess
        subprocessVideo.send_signal(signal.SIGINT)  # Sends the interrupt signal (Ctrl+C)
        # If the process does not terminate, force kill it
        if subprocessVideo.poll() is None:  # Check if the process is still running
            subprocessVideo.kill()  # Force kill the process
        # Wait for the process to terminate and get the exit code
        exit_code = subprocessVideo.wait()
        print(f"Process exited with code {exit_code}")

        update.message.reply_text("Video streaming stopped")     



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
    return switcher.get(message, Handle_Received_Unknown)


    
def HandleReceived(update):
    """
    Call Corresponding handler for the received message
    """
    ReceivedMessageHandler(update.message.text)(update)

