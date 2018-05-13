from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import bot_parser

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
    update.message.reply_text('Help!')


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text('''В Москве на проспекте Академика Сахарова прошла акция партии ПАРНАС в поддержку заблокированного Роскомнадзором мессенджера Telegram, передает корреспондент РБК. Сбор участников начался в 13:00 мск на улице Маши Порываевой возле станции метро «Комсомольская».
В митинге, как следует из заявки организаторов, <a href="https://www.rbc.ru/society/08/05/2018/5af19cc29a7947809dc5fc7d">должны были принять участие</a> до 5 тыс. человек. К 14:30 мск, по данным занимающегося подсчетом людей на массовых мероприятиях проекта «Белый счетчик», на территорию проведения акции<a href="https://twitter.com/WhiteCounter/status/995629819672002560" target="_blank"> прошли</a> 1,69 тыс. участников. На 14:45 представители проекта<a href="https://twitter.com/WhiteCounter/status/995632638131044352" target="_blank"> оценивали </a>численность митингующих уже в 1,97 тыс. человек. В пресс-службе главного управления МВД по Москве РБК сообщили, что пока не обладают информацией о количестве участников мероприятия. К 15:15 мск в полиции <a href="https://77.xn--b1aew.xn--p1ai/news/item/13055978" target="_blank">оценили</a> число митингующих примерно в 1 тыс. человек. На 15:45 мск, по данным «Белого счетчика, на территорию митинга <a href="https://twitter.com/WhiteCounter/status/995648510925172736" target="_blank">прошли</a> 2,40 тыс. человек.
Участники акции шли с плакатами с надписями: «Роскомпозор», «Помоги Даше найти здравый смысл», «Товарищ, требуй свободу интернета» и «Эй, РКН, где же свобода общения?» У сцены — флаги партий «Яблоко» и ПАРНАС. Также у некоторых пришедших на митинг в руках российский триколор.
Со сцены, как передает корреспондент РБК, звучат лозунги: «Хватит ломать Рунет!» и «Цензуре — нет!» «Блокировки соцсетей — огромный удар по IT-компаниям, они потеряли столько денег. И это вопрос не о деньгах, а о доверии. Зачем таким компаниям вести бизнес здесь [в России], платить тут налоги, если можно все перенести в другие страны? В нашей стране убивают наше будущее», — объявил, выступая на митинге, один из организаторов акции, председатель движения «Открытая Россия» Андрей Пивоваров.
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
</span>
</span>
</a>
<div class="article__photoreport__bottom">
<a class="article__photoreport__category" href="/multimedia">
            Фотогалерея
        </a>
<span class="icons__photo"></span>
</div>
</div>

Позже член ПАРНАСа Андрей Кузнецов сообщил РБК о 15 задержанных участниках акции. В пресс-службе ГУ МВД по Москве РБК комментировать эту информацию отказались.
Первая акция «За свободный интернет» в столице состоялась 30 апреля. Тогда она была организована Либертарианской партией, также среди соорганизаторов мероприятия была указана команда оппозиционера, основателя Фонда борьбы с коррупцией (ФБК) Алексея Навального. Первый митинг также прошел на проспекте Сахарова. При его согласовании организаторы указали число участников в 5 тыс. человек. Однако участие в митинге приняло большее количество человек. По оценкам московской полиции, митинг посетили 7,5 тыс. человек. Проект «Белый счетчик» в свою очередь<a href="https://twitter.com/WhiteCounter/status/991023927576100864" target="_blank"> насчитал</a> 12,3 тыс. участников.
Обе акции «За свободный интернет» — и в апреле, и в мае — организованы в столице в связи с блокировкой в России Роскомнадзором Telegram. Такое постановление из-за отказа администрации мессенджера выдать ФСБ ключи шифрования переписки пользователей вынес московский Таганский суд. Блокировку мессенджера Роскомнадзор начал 16 апреля. После этого Telegram перешел на разные наборы IP-адресов, которые также начало блокировать ведомство. Так, проблемы с доступом испытывали пользователи соцсетей «ВКонтакте», «Одноклассники», поисковика Google и почты Gmail.''')


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
