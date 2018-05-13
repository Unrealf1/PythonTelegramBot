from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import re
import peewee
import bot_parser
db = peewee.SqliteDatabase('news.db')
status = "Initializing"


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text("How can I help you?")


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def new_docs(bot, update):
    inp = update.message.text.split()
    if len(inp) == 2:
        if status != "working":
            update.message.reply_text("I'm sorry, now updating...")
        else:
            amount = int(inp[1])
            bot_parser.Themes.create_table()
            bot_parser.Docs.create_table()
            out_docs = bot_parser.Docs.select().order_by(bot_parser.Docs.last_update.desc()).limit(amount)
            for doc in out_docs:
                '''name = peewee.CharField(null=False)
                    theme = peewee.CharField(null=False)
                    description = peewee.CharField(null=True)
                    link = peewee.CharField(null=False)'''
                update.message.reply_text("Name: " + doc.name + "\nOn theme: " + doc.theme + "\nDescription: " + doc.description + "\nSourse: " + doc.link + "\nLast updated: " + str(doc.last_update))

    else:
        update.message.reply_text("Incorrect input")


def new_themes(bot, update):
    inp = update.message.text.split()
    if len(inp) == 2:
        if status != "working":
            update.message.reply_text("I'm sorry, now updating...")
        else:
            amount = int(inp[1])
            bot_parser.Themes.create_table()
            out_themes = bot_parser.Themes.select().order_by(bot_parser.Themes.last_update.desc()).limit(amount)
            for theme in out_themes:
                '''name = peewee.CharField(null=False)
                    theme = peewee.CharField(null=False)
                    description = peewee.CharField(null=True)
                    link = peewee.CharField(null=False)'''
                update.message.reply_text("Name: " + theme.name + "\nDescription: " + theme.description + "\nSourse: " + theme.link_rbc + "\nLast updated: " + str(theme.last_update))

    else:
        update.message.reply_text("Incorrect input")


def upd(bot, update):
    inp = update.message.text.split()
    if len(inp) == 2:
        if inp[1] == '3691':
            global status
            update.message.reply_text("Going to update, master")
            status = "updating"
            bot_parser.pars_main()
            status = "working"


def get_status(bot, update):
    inp = update.message.text.split()
    if len(inp) == 2:
        if inp[1] == '3691':
            update.message.reply_text(status)


def main():
    global status
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater('591724946:AAEj1zLLO9zP6Sc2sWjLePR4siqTHPoJXVs')

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("new_docs", new_docs))
    dp.add_handler(CommandHandler("new_themes", new_themes))
    dp.add_handler(CommandHandler("update", upd))
    dp.add_handler(CommandHandler("get_status", get_status))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    status = "working"
    updater.idle()


if __name__ == '__main__':
    main()
