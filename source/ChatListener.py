"""
Telegram Chat Bot handler
"""

import ChatMessager
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


def CallbackTelegramReceivedMessage(update: Update, context: CallbackContext) -> None:
    """
    Called when new telegram message received
    """
    print("Telegram_Rx:" + update.message.text)
    ChatMessager.HandleReceived(update)


def Init(telegram_token):
    """
    Initialize telegram bot to process and respond to received messages
    """
    # Create the Updater and pass it your bot's token.
    updater = Updater(telegram_token)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    # Register message handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, CallbackTelegramReceivedMessage))
    # Start the Bot
    updater.start_polling()
    updater.idle()

    ChatMessager.init()

