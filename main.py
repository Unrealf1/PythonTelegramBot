from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

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
    update.message.reply_text('''<html><body>Постоянное представительство России при Организации по запрещению химического оружия (ОЗХО) получило ответы на свои вопросы, которые возникли после публикации ОЗХО доклада по «делу Скрипаля». Об этом  сообщил постпред России при организации Александр Шульгин.
«У нас возникли вопросы к этому докладу, в частности, складывалось впечатление, что эксперты организации искали только то вещество, которое указали британцы. Непонятно было, откуда взялся [химикат] BZ, почему нужно было проверять сертифицированную лабораторию, посылать туда контрольную пробу», — сказал он.


        Спор на новом уровне: чего ждать Москве от доклада ОЗХО о «деле Скрипаля»
    


            Политика
        


По словам Шульгина, ответ ОЗХО — «сугубо технический», его необходимо изучить на экспертном уровне. «Дальше мы будем уже определяться», — добавил он. Как отметил дипломат, по данным российской стороны, ОЗХО сейчас «не играет никакой роли в расследовании инцидента в Солсбери».


        Лавров рассказал о признаках отравления Скрипалей веществом BZ
    


            Политика
        

</div>
Группа экспертов ОЗХО по запросу Лондона начала расследование «дела Скрипаля» в середине марта. 11 апреля организация передала полную версию отчета Великобритании. На следующий день по просьбе британской стороны ОЗХО распространила рассекреченное резюме документа.
В организации подтвердили, что при отравлении бывшего полковника ГРУ Сергея Скрипаля и его дочери Юлии <a href="https://www.rbc.ru/politics/12/04/2018/5acf2ccc9a794721fa1bfbcd">было использовано</a> нервно-паралитическое вещество «Новичок». При этом ОЗХО происхождение этого яда не установила. Кроме того, эксперты <a href="https://www.rbc.ru/politics/18/04/2018/5ad73ccf9a7947ef075fa037">не обнаружили</a> в пробах, которые они отобрали на месте отравления Скрипалей, следов химического вещества BZ.
Сергей Скрипаль и Юлия были обнаружены в британском городе Солсбери 4 марта. Они были в бессознательном состоянии. Власти Великобритании считают Москву причастной к их отравлению «Новичком». Кремль все обвинения отрицает.</body></html>
''')


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater('591724946:AAEj1zLLO9zP6Sc2sWjLePR4siqTHPoJXVs')

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
