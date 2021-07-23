from datetime import datetime, timedelta
from jobs import hourly_db_repopulation
import logging
import settings

from telegram.bot import Bot
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler,
                          CallbackQueryHandler)
from telegram.ext import messagequeue as mq
from telegram.utils.request import Request

from handlers import (greeting, echo, default_currency_handler, default_currency_reply,
                      list_crypto, list_currency, list_stocks, populate_DB)

PROXY = {'proxy_url': settings.PROXY_URL, 
         'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

logging.basicConfig(filename="bot.log", level=logging.INFO)


class MQBot(Bot):
    def __init__(self, *args, is_queued_def=True, msg_queue=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = msg_queue or mq.MessageQueue()

    def stop(self):
        try:
            self._msg_queue.stop()
        except:
            pass

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        return super().send_message(*args, **kwargs)


def main():
    request = Request(
        con_pool_size=8,
        proxy_url=PROXY['proxy_url'],
        urllib3_proxy_kwargs=PROXY['urllib3_proxy_kwargs']
    )

    
    bot = MQBot(settings.API_KEY, request=request)
    mybot = Updater(bot=bot, use_context=True)

    nearest_round_hour = datetime.now() + (datetime.min - datetime.now()) % timedelta(minutes=60)
    jq = mybot.job_queue
    jq.run_repeating(hourly_db_repopulation, interval=3600, first=nearest_round_hour)

    
    dp=mybot.dispatcher
    dp.add_handler(CommandHandler("start", greeting))
    dp.add_handler(MessageHandler(Filters.regex('^(Валюта по умолчанию)$'), default_currency_handler))
    dp.add_handler(MessageHandler(Filters.regex('^(Курсы валют)$'), list_currency))
    dp.add_handler(MessageHandler(Filters.regex('^(Курсы крипто)$'), list_crypto))
    dp.add_handler(MessageHandler(Filters.regex('^(Курсы акций)$'), list_stocks))
    dp.add_handler(MessageHandler(Filters.regex('^(заполнить базу)$'), populate_DB))
    dp.add_handler(CallbackQueryHandler(default_currency_reply, pattern='^(default|)'))
#    dp.add_handler(CallbackQueryHandler(sub_currency, pattern='^(sub_cur|)'))
#    dp.add_handler(CallbackQueryHandler(sub_crypto, pattern='^(sub_crypto|)'))
#    dp.add_handler(CallbackQueryHandler(sub_stocks, pattern='^(sub_stock|)'))
    dp.add_handler(MessageHandler(Filters.text, echo))

    logging.info("Бот стартовал ")

    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()