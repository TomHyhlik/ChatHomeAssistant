"""
Telegram Chat Bot handler
"""

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


LOG_NAME = "TEL "


class TelegramChatCommunicator:
    def __init__(self, telegram_token):
        self.telegram_token = telegram_token
        pass

    def register_callback_on_received_message(self, callback):
        self.on_received_message = callback


    def __callback_message_received(self, handle: Update, context: CallbackContext) -> None:
        """
        Called when new telegram message received
        """
        print(LOG_NAME + "message received:\t" + handle.message.text)
        self.on_received_message(handle, handle.message.text)


    def send_reply_message_text(self, handle, message):
        print(LOG_NAME + "message send:\t" + message)
        handle.message.reply_text(message)


    def send_reply_message_photo(self, handle, file):
        print(LOG_NAME + "photo send")
        handle.message.reply_photo(file)


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
