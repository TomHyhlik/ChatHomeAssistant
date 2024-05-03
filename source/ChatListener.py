import messageHandler


import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


def ReceivedMessageHandler(update: Update, context: CallbackContext) -> None:
    """
    Handle received telegram message
    """
    print("Telegram_Rx:" + update.message.text)
    messageHandler.handleRx(update)


def Init(telegram_token):
    """
    Initialize telegram bot, listening
    """
    # Create the Updater and pass it your bot's token.
    updater = Updater(telegram_token)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    # Register message handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, ReceivedMessageHandler))
    # Start the Bot
    updater.start_polling()
    updater.idle()

