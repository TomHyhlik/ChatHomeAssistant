#!/usr/bin/env python3

import telegram_send
import ChatCommunicator
import AppConfig
import time
import ChatMessager


LOG_NAME = "MAI "

def telegram_send_init_message(message):
    print(LOG_NAME + " message send: "+ message)
    telegram_send.send(messages=[message])   

def AppInit() -> None:
    telegram_send_init_message("Bot on")
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

