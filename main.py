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
    update.message.reply_text('''В Москве на проспекте Академика Сахарова прошла акция партии ПАРНАС в поддержку заблокированного Роскомнадзором мессенджера Telegram, передает корреспондент РБК. Сбор участников начался в 13:00 мск на улице Маши Порываевой возле станции метро «Комсомольская».
Пивоваров.
<div class="article__inline-material">
<a class="article__inline-material__title" href="https://www.rbc.ru/society/08/05/2018/5af19cc29a7947809dc5fc7d">
        Вторая акция в поддержку Telegram пройдет 13 мая на проспекте Сахарова
    </a>
<div class="article__inline-material__bottom">
<a class="article__inline-material__category" href="/society">
            Общество
        </a>
</div>
</div>​
Также на мероприятии присутствует председатель ПАРНАСа​ Михаил Касьянов. «Мы должны поддержать [основателя Telegram Павла] Дурова в борьбе за свободу интернета и Telegram, продолжать выходить на митинги и дальше», — призвал он.
Разблокировать мессенджер, возместить его владельцам ущерб от его блокировки и отправить в отставку Роскомнадзор со сцены потребовала другой организатор митинга, председатель партии «Яблоко» Эмилия Слабунова.​ Толпа откликнулась на ее призывы криками: «Надоел!» и «Свобода СМИ!»

<div class="article__photoreport">
<a class="article__photoreport__title" href="https://www.rbc.ru/photoreport/13/05/2018/5af82f309a79476510244366">
        Второй митинг в поддержку Telegram в Москве. Фоторепортаж
        <span class="article__photoreport__image-container">
<span class="article__photoreport__image-wrap">
<span class="article__photoreport__image-wrap__inner">
<img class="article__photoreport__image" src="https://s0.rbk.ru/v6_top_pics/resized/240x120_crop/media/img/4/42/755262148081424.jpg"/>
</span>
</span>
<span class="article__photoreport__image-wrap">
<span class="article__photoreport__image-wrap__inner">
<img class="article__photoreport__image" src="https://s0.rbk.ru/v6_top_pics/resized/240x120_crop/media/img/6/62/755262150285626.jpg"/>
</span>
</span>
<span class="article__photoreport__image-wrap">
<span class="article__photoreport__image-wrap__inner">
<img class="article__photoreport__image" src="https://s0.rbk.ru/v6_top_pics/resized/240x120_crop/media/img/1/18/755262148080181.jpg"/>
</span>
</span>
<span class="article__photoreport__image-wrap">
<span class="article__photoreport__image-wrap__inner last">
<img class="article__photoreport__image" src="https://s0.rbk.ru/v6_top_pics/resized/240x120_crop/media/img/3/30/755262154301303.jpg"/>
<span class="article__photoreport__more">Еще 5 фото</span>
</span>
</a>
<div class="article__photoreport__bottom">
<a class="article__photoreport__category" href="/multimedia">
            Фотогалерея
        </a>
<span class="icons__photo"></span>
</div>
</div>''')


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
