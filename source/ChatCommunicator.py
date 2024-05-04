"""
Telegram Chat Bot handler
"""

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext



class TelegramChatCommunicator:
    def __init__(self, telegram_token):
        self.telegram_token = telegram_token
        pass

    def register_callback_on_received_message(self, callback):
        self.on_received_message = callback


    def __callback_message_received(self, update: Update, context: CallbackContext) -> None:
        """
        Called when new telegram message received
        """
        print("Telegram received:\t" + update.message.text)
        self.on_received_message(update, update.message.text)


    def message_reply(self, handle, message):
        print("Telegram send:\t" + message)
        handle.message.reply_text(message)


    def listen(self, ):
        """
        Initialize telegram bot to process and respond to received messages
        """
        # Create the Updater and pass it your bot's token.
        updater = Updater(self.telegram_token)
        # Get the dispatcher to register handlers
        dispatcher = updater.dispatcher
        # Register message handler
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.__callback_message_received))
        # Start the Bot
        updater.start_polling()
        updater.idle()
