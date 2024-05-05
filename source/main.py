#!/usr/bin/env python3

import telegram_send
import ChatCommunicator
import AppConfig
import time
import threading
import ChatMessager
import PirHandler

APP_CONFIG_FILE = "/home/pi/Repos/ChatHomeAssistant/source/AppConfig.py"

LOG_NAME = "MAI "

def telegram_send_message(message):
    print(LOG_NAME + " message send:\t" + message)
    telegram_send.send(messages=[message])   

def handle_pir_trigger():
    telegram_send_message("Motion detected!")

def AppInit() -> None:
    telegram_send_message("Chat Home Asistant Started")
    # Telegram send whole app configuration
    with open(APP_CONFIG_FILE, 'r') as configFile:
        configContent = configFile.read()
        telegram_send_message(configContent)
    if AppConfig.AppConfig['pir_sensor_enabled']:
        pirHandler = PirHandler.PirHandler(int(AppConfig.AppConfig['pir_sensor_gpio']))
        pirHandler.register_callback(handle_pir_trigger)
        # Run the PirHandler in thread so it is not blocking
        thread = threading.Thread(target=pirHandler.start)
        thread.start()
    # Create telegram chat communicator
    chatCOmmunicator = ChatCommunicator.TelegramChatCommunicator(AppConfig.AppConfig['telegram_token'])
    # Create message handler
    chatMessager = ChatMessager.ChatMessager(chatCOmmunicator)
    # Start the chat bot listening
    chatCOmmunicator.listen()


def main() -> None:
    if (AppConfig.AppConfig['debug']):
        AppInit()
    else:
        while True:
            try:    
                AppInit()
                break
            except:
                print(LOG_NAME +" Failed to init telegram bot")
                time.sleep(10)
        
if __name__ == '__main__':
    main()

