#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging
import settings
from uuid import uuid4
from web3 import Web3

import requests
import secrets

from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram import InlineTotalityMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext
)
from telegram.utils.helpers import escape_markdown
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

HANDLE, ERC20 = range(2)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi, this bot lets you create a Totality bot')
    update.message.reply_text("What is the handle of your bot? (e.g. @mycoolbot)")
    return HANDLE

def handle(update, context):
    handle = update.message.text
    context.user_data["handle"] = handle
    update.message.reply_text(
        "Great, which ERC20 do you want to use?",
        reply_markup=ReplyKeyboardMarkup([['DAI', 'USDC']], one_time_keyboard=True),
    )
    return ERC20

def erc20(update, context):
    user_data = context.user_data
    handle = user_data.get("handle")
    if not handle:
        update.message.reply_text("Something when wrong, please press /cancel")
        return
    del user_data["handle"]

    secret = secrets.token_urlsafe(58)[:58]

    erc20 = update.message.text
    r = requests.post("%s/bot" % settings.TOTALITY, data={
        "secret": secret,
        "handle": handle,
        "contact_handle": update.effective_user.username,
        "erc20": erc20
    })
    if r.status_code is not 200:
        update.message.reply_text("Something when wrong, please press /cancel")
        return

    update.message.reply_text("Registered bot %s to use %s, please use the following secret: \n\n%s" % (handle, erc20, secret))

    return ConversationHandler.END

def cancel(update, context):
    return ConversationHandler.END

def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(settings.BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            HANDLE: [MessageHandler(Filters.regex('(@[A-Z a-z])\w+'), handle)],
            ERC20: [MessageHandler(Filters.regex('^(DAI|USDC)$'), erc20)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    # on different commands - answer in Telegram
    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
