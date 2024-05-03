#!/usr/bin/env python3

import telegram_send
import ChatListener
import AppConfig
import time


def telegram_sendMessage(message):
    print("main\ttelegram send: "+ message)
    telegram_send.send(messages=[message])   


def AppInit() -> None:
    telegram_sendMessage("Bot on")
    ChatListener.init(AppConfig.AppConfig['telegram_token'])


def main() -> None:
    if (AppConfig.AppConfig['debug']):
        AppInit()
    else:
        while True:
            try:    
                AppInit()
                break
            except:
                print("Failed to init telegram bot")
                time.sleep(10)
        
if __name__ == '__main__':
    main()

