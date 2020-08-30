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

from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram import InlineTotalityMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackQueryHandler
from telegram.utils.helpers import escape_markdown
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi, this bot lets you send payment requests inside Telegram!')
    if not update.effective_user.address:
        update.message.reply_text("You did not link your Ethereum address to your telegram account yet, "
                "please download the Totality fork or get in contact with @custodialbot")
        return

    keyboard = [[InlineKeyboardButton("Select chat", switch_inline_query='1')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Send a payment request inside a chat!', reply_markup=reply_markup)

def handle_inline_result(update, context):
    query = update.callback_query
    if query.data.startswith("tg"):
        if context.totality["canceled"]:
            if context.totality["tx"]:
                return query.edit_message_text(
                    text="Oops.. you canceled the transaction but: <i>%s</i>, is found" % context.totality["tx"]["tx"],
                    parse_mode="HTML")
            return query.edit_message_text(text="The transaction is canceled")

        if not context.totality["tx"]:
            query.answer(text="Please click on custodial bot")
        else:
            query.edit_message_text(
                text="Great! The transaction is pending. hash: <i>%s</i>" % context.totality["tx"]["tx"],
                parse_mode="HTML")
        return

def inlinequery(update, context):
    """Handle the inline query."""
    if not update.effective_user.address:
        update.inline_query.answer([], switch_pm_text="Get started", switch_pm_parameter="start")
        return

    query = update.inline_query.query
    try:
        query = round(float(query), 2)
        if query > 500:
            query = 500
    except ValueError:
        query = 1.0

    keyboard = InlineTotalityMarkup(
        settings.DAI_CONN.functions.transfer(
            update.effective_user.address,
            Web3.toWei(query, "ether")
        ), # contract function
        Web3.toWei("2", "gwei"), # gasprice
        500000 # amount of gas
    )

    results = [
        InlineQueryResultArticle(
            id=query,
            title="Request %s DAI" % query,
            thumb_url="https://engamb.sfo2.digitaloceanspaces.com/wp-content/uploads/2019/10/09141745/NEW-dai-logo-e1570610882413.png",
            description="One person is able to pay the requested amount.",
            input_message_content=InputTextMessageContent("Im requesting %s DAI" % query),
            reply_markup=keyboard
        )
    ]

    update.inline_query.answer(results, cache_time=10, is_personal=True)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(settings.BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(handle_inline_result))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
