"""
Telegram Chat Bot handler
"""

import ChatMessager
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext



class ChatListener:
    def __init__(self):
        self.chatMessager = None


    def CallbackTelegramReceivedMessage(self, update: Update, context: CallbackContext) -> None:
        """
        Called when new telegram message received
        """
        print("Telegram_Rx:" + update.message.text)
        self.chatMessager.handle_received_message(update)

    def listen(self, telegram_token):
        """
        Initialize telegram bot to process and respond to received messages
        """
        self.chatMessager = ChatMessager.ChatMessager()

        # Create the Updater and pass it your bot's token.
        updater = Updater(telegram_token)
        # Get the dispatcher to register handlers
        dispatcher = updater.dispatcher
        # Register message handler
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.CallbackTelegramReceivedMessage))
        # Start the Bot
        updater.start_polling()
        updater.idle()
