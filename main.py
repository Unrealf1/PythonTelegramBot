from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import re
import peewee
import bot_parser
import collections
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
    update.message.reply_text('''commands:
/help - показать все, что может бот
/new_docs <N> - показать N самых свежих новостей
/new_topics <N> - показать N самых свежих тем
/topic <topic_name> - показать описание темы и заголовки 5 самых свежих новостей в этой теме
/doc <doc_title> - показать текст документа с заданным заголовком
/words <topic_name> - показать 5 слов, лучше всего характеризующих тему. Алгоритм оценки слов выберите/придумайте сами
/describe_doc <doc_title> - вывести статистику по документу.
/describe_topic <topic_name> - вывести статистику по теме.
''')


def echo(bot, update):
    """Echo the user message."""
    if len(update.message.text) > 0 and update.message.text[0] == '/':
        update.message.reply_text("Oh, don't now what to do!\nPlease, try /help to know my powers")
    else:
        update.message.reply_text("Sorry, I can't talk now...\nTry /help to know my powers!")


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


def new_topics(bot, update):
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


def topic(bot, update):
    name = (update.message.text[len("/topic"):]).strip()
    if len(name) > 0:
        if status != "working":
            update.message.reply_text("I'm sorry, now updating...")
        else:
            bot_parser.Docs.create_table()
            out_docs = bot_parser.Docs.select().where(bot_parser.Docs.theme == name).limit(5)

            if len(out_docs) == 0:
                update.message.reply_text("Sorry, no topics on this theme")
            for doc in out_docs:
                '''name = peewee.CharField(null=False)
                    theme = peewee.CharField(null=False)
                    description = peewee.CharField(null=True)
                    link = peewee.CharField(null=False)'''
                update.message.reply_text("Name: " + doc.name + "\nOn theme: " + doc.theme + "\nDescription: " + doc.description + "\nSourse: " + doc.link + "\nLast updated: " + str(doc.last_update))

    else:
        update.message.reply_text("Enter topic name")


def get_doc(bot, update):
    name = (update.message.text[len("/doc"):]).strip()
    if len(name) > 0:
        if status != "working":
            update.message.reply_text("I'm sorry, now updating...")
        else:
            bot_parser.Docs.create_table()
            out_docs = bot_parser.Docs.select().where(bot_parser.Docs.name == name).limit(1)

            if len(out_docs) == 0:
                update.message.reply_text("Sorry, no topics with this name")
            for doc in out_docs:
                '''name = peewee.CharField(null=False)
                    theme = peewee.CharField(null=False)
                    description = peewee.CharField(null=True)
                    link = peewee.CharField(null=False)'''
                update.message.reply_text(
                    "Name: " + doc.name + "\nOn theme: " + doc.theme + "\nDescription: " + doc.description + "\nSourse: " + doc.link + "\nLast updated: " + str(
                        doc.last_update))

    else:
        update.message.reply_text("Enter doc name")


def get_words(bot, update):
    name = (update.message.text[len("/words"):]).strip()
    if len(name) > 0:
        if status != "working":
            update.message.reply_text("I'm sorry, now updating...")
        else:
            bot_parser.Docs.create_table()
            bot_parser.Tegs.create_table()
            bot_parser.Themes.create_table()
            words = collections.defaultdict(int)
            out_docs = bot_parser.Docs.select().where(bot_parser.Docs.theme == name).limit(20)

            if len(out_docs) == 0:
                update.message.reply_text("Sorry, no topics with this name")
            for doc in out_docs:
                for teg in bot_parser.Tegs.select().where(bot_parser.Tegs.link == doc.link):
                    words[teg.teg] += 1

            srt = sorted(words, key=words.get)
            answer = 'words are: '
            for i in range(min(len(srt), 5)):
                answer += srt[i] + ', '
            update.message.reply_text(answer + '.')

    else:
        update.message.reply_text("Enter topic name")


def main():
    global status
    """Start the bot."""
    # Create the EventHandler
    updater = Updater('591724946:AAEj1zLLO9zP6Sc2sWjLePR4siqTHPoJXVs')

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("new_docs", new_docs))
    dp.add_handler(CommandHandler("new_topics", new_topics))
    dp.add_handler(CommandHandler("update", upd))
    dp.add_handler(CommandHandler("get_status", get_status))
    dp.add_handler(CommandHandler("topic", topic))
    dp.add_handler(CommandHandler("doc", get_doc))
    dp.add_handler(CommandHandler("words", get_words))
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
