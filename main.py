from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import re
import peewee
import bot_parser
import collections
import supply_func


DEFAULT_NUMBER_OF_TOPICS = 5
DEFAULT_NUMBER_OF_DOCS = 5

DEFAULT_MAINTENANCE_ANSWER = "Извините, в данный момент я не готов " \
                                      "ответить на запрос... Скорее всего в " \
                                      "течении 20 минут проблема будет " \
                                      "исправлена!"

db = peewee.SqliteDatabase('news.db')
status = "Initializing"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s'
                           ' - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Response to /start command
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


# Response to /help command
def bot_help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('''Доступные действия:
/help - показать все, что может бот
/new_docs <N> - показать N самых свежих новостей
/new_topics <N> - показать N самых свежих тем
/topic <topic_name> - показать описание темы и заголовки 5 самых свежих новостей в этой теме
/doc <doc_title> - показать текст документа с заданным заголовком
/words <topic_name> - показать 5 слов, лучше всего характеризующих тему.
/describe_doc <doc_title> - вывести статистику по документу.
/describe_topic <topic_name> - вывести статистику по теме.
''')


# Response to not command message
def echo(bot, update):
    """Send a message when user request is not a command"""
    if len(update.message.text) > 0:
        update.message.reply_text("Sorry, I don't understand you...\n"
                                  "Try /help to know my powers!")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


# Response to /new_docs command
def new_docs(bot, update):
    inp = update.message.text.split()
    if len(inp) <= 2:
        if status != "working":
            update.message.reply_text(DEFAULT_MAINTENANCE_ANSWER)
        else:
            if len(inp) == 1:
                amount = DEFAULT_NUMBER_OF_DOCS
            else:
                amount = int(inp[1])

            bot_parser.Docs.create_table()
            out_docs = bot_parser.Docs.select().order_by(
                bot_parser.Docs.last_update.desc()).limit(amount)
            for doc in out_docs:
                update.message.reply_text("Название: " + doc.name + "\nТема: "
                                          + doc.theme + "\nОписание: "
                                          + doc.description + "\nИсточник: "
                                          + doc.link
                                          + "\nПоследнее обновление: "
                                          + str(doc.last_update))

    else:
        update.message.reply_text(DEFAULT_MAINTENANCE_ANSWER)


# Response to /new_topics command
def new_topics(bot, update):
    inp = update.message.text.split()
    if len(inp) <= 2:
        if status != "working":
            update.message.reply_text(DEFAULT_MAINTENANCE_ANSWER)
        else:
            if len(inp) == 1:
                amount = DEFAULT_NUMBER_OF_DOCS
            else:
                amount = int(inp[1])

            bot_parser.Themes.create_table()
            out_themes = bot_parser.Themes.select().order_by(
                bot_parser.Themes.last_update.desc()).limit(amount)
            for theme in out_themes:
                update.message.reply_text("Название: " + theme.name +
                                          "\nОписание: " +
                                          theme.description +
                                          "\nИсточник: " + theme.link_rbc +
                                          "\nПоследнее обновление: " +
                                          str(theme.last_update))

    else:
        update.message.reply_text("Введите команду в формате '/new_topics n', "
                                  "где n - это количество тем, которые "
                                  "Вы хотите получить.")


# function for remote database update
def upd(bot, update):
    inp = update.message.text.split()
    if len(inp) == 2:
        if inp[1] == '3691':
            global status
            update.message.reply_text("Going to update, master")
            status = "updating"
            bot_parser.pars_main()
            update.message.reply_text("Update finished")
            status = "working"


# function for remote database status
def get_status(bot, update):
    inp = update.message.text.split()
    if len(inp) == 2:
        if inp[1] == '3691':
            update.message.reply_text(status)


# Response to /topic command
def topic(bot, update):
    name = (update.message.text[len("/topic"):]).strip()
    if len(name) > 0:
        if status != "working":
            update.message.reply_text(DEFAULT_MAINTENANCE_ANSWER)
        else:
            bot_parser.Docs.create_table()
            out_docs = bot_parser.Docs.select().where(bot_parser.Docs.theme ==
                                                      name).limit(5)

            if len(out_docs) == 0:
                update.message.reply_text("Извините, но по теме %s у меня "
                                          "новостей нет" % name)
            for doc in out_docs:
                update.message.reply_text("Название: " + doc.name + "\nТема: "
                                          + doc.theme + "\nОписание: "
                                          + doc.description + "\nИсточник: "
                                          + doc.link
                                          + "\nПоследнее обновление: "
                                          + str(doc.last_update))

    else:
        update.message.reply_text("Введите комманду в формате /topic name,"
                                  " где name - имя интересующей Вас темы ")


# Response to /doc command
def get_doc(bot, update):
    name = (update.message.text[len("/doc"):]).strip()
    if len(name) > 0:
        if status != "working":
            update.message.reply_text(DEFAULT_MAINTENANCE_ANSWER)
        else:
            bot_parser.Docs.create_table()
            out_docs = bot_parser.Docs.select().where(bot_parser.Docs.name
                                                      == name).limit(1)

            if len(out_docs) == 0:
                update.message.reply_text("Извините, но я не знаю новостей с "
                                          "таким названием")
            for doc in out_docs:
                update.message.reply_text(
                    doc.text + "\nПоследнее обновление: " + str(
                        doc.last_update))

    else:
        update.message.reply_text("Введите комманду в формате /doc name, где "
                                  "name - имя интересующей Вас новости")


# Response to /words command
def get_words(bot, update):
    name = (update.message.text[len("/words"):]).strip()
    if len(name) > 0:
        if status != "working":
            update.message.reply_text(DEFAULT_MAINTENANCE_ANSWER)
        else:
            bot_parser.Docs.create_table()
            bot_parser.Tegs.create_table()
            bot_parser.Themes.create_table()
            words = collections.defaultdict(int)
            out_docs = bot_parser.Docs.select().where(
                bot_parser.Docs.theme == name).limit(20)

            if len(out_docs) == 0:
                update.message.reply_text("Извините, но я не знаю новотной "
                                          "темы с таким названием")
            for doc in out_docs:
                for teg in bot_parser.Tegs.select().where(
                        bot_parser.Tegs.link == doc.link):
                    words[teg.teg] += 1

            srt = sorted(words, key=words.get)
            answer = 'Слова, характеризующие тему: '
            for i in range(min(len(srt), 5)):
                answer += srt[i] + ', '
            update.message.reply_text(answer[:-1])

    else:
        update.message.reply_text("Введите комманду в формате /words name, "
                                  "где name - имя интересующей Вас темы")


# Response to /describe_doc command
def describe_doc(bot, update):
    name = (update.message.text[len("/describe_doc"):]).strip()
    if len(name) > 0:
        if status != "working":
            update.message.reply_text(DEFAULT_MAINTENANCE_ANSWER)
        else:
            bot_parser.Docs.create_table()
            out_docs = bot_parser.Docs.select().where(
                bot_parser.Docs.name == name).limit(1)

            if len(out_docs) == 0:
                update.message.reply_text("Извините, но я не знаю новотной"
                                          " темы с таким названием")
            word_statistics = collections.defaultdict(int)
            len_statistics = collections.defaultdict(int)
            for doc in out_docs:
                words = re.findall(r'\w+', doc.text)
                for word in words:
                    word_statistics[word] += 1
                    len_statistics[len(word)] += 1

            plots = supply_func.get_plots(word_statistics, len_statistics)

            chat_id = update["message"]["chat"]["id"]

            for plot in plots:
                bot.send_photo(chat_id=chat_id, photo=open(plot, "rb"))

            supply_func.clear_plots(plots)

    else:
        update.message.reply_text("Введите комманду в формате /describe_doc "
                                  "name, где name - имя интересующей Вас "
                                  "новости")


# Response to /describe_topic command
def describe_topic(bot, update):
    name = (update.message.text[len("/describe_topic"):]).strip()
    if len(name) > 0:
        if status != "working":
            update.message.reply_text(DEFAULT_MAINTENANCE_ANSWER)
        else:
            bot_parser.Docs.create_table()
            out_docs = bot_parser.Docs.select().where(
                bot_parser.Docs.theme == name)
            if len(out_docs) == 0:
                update.message.reply_text("Извините, но я не знаю новотной"
                                          " темы с таким названием")
                return

            word_statistics = collections.defaultdict(int)
            len_statistics = collections.defaultdict(int)
            doc_len_statistics = collections.defaultdict(int)
            for doc in out_docs:
                words = re.findall(r'\w+', doc.text)
                doc_len_statistics[len(words)] += 1
                for word in words:
                    word_statistics[word] += 1
                    len_statistics[len(word)] += 1

            plots = supply_func.get_plots(word_statistics, len_statistics)
            super_plot = supply_func.get_docs_plot(doc_len_statistics)

            chat_id = update["message"]["chat"]["id"]
            update.message.reply_text('В теме %d документов' % len(out_docs))
            for plot in plots:
                bot.send_photo(chat_id=chat_id, photo=open(plot, "rb"))

            supply_func.clear_plots((plots[0], plots[1], super_plot))

    else:
        update.message.reply_text("Введите комманду в формате /describe_topic "
                                  "name, где name - имя интересующей Вас "
                                  "новости")


def main():
    global status
    """Start the bot."""
    # Create the EventHandler
    updater = Updater('591724946:AAEj1zLLO9zP6Sc2sWjLePR4siqTHPoJXVs')

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", bot_help))
    dp.add_handler(CommandHandler("new_docs", new_docs))
    dp.add_handler(CommandHandler("new_topics", new_topics))
    dp.add_handler(CommandHandler("update", upd))
    dp.add_handler(CommandHandler("get_status", get_status))
    dp.add_handler(CommandHandler("topic", topic))
    dp.add_handler(CommandHandler("doc", get_doc))
    dp.add_handler(CommandHandler("words", get_words))
    dp.add_handler(CommandHandler("describe_doc", describe_doc))
    dp.add_handler(CommandHandler("describe_topic", describe_topic))

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
