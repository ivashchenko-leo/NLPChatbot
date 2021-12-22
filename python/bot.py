import telebot
import python.chat
import logging.config
from python import datasource
import signal


API_KEY = '5083139604:AAGcd0m6UhBkNmxIu78Nv2c53c0Q4lg8r14'
LANGUAGES = ['EN', 'RU']


def run():
    logging.config.fileConfig("../logging.conf")
    logger = logging.getLogger()

    bot = telebot.TeleBot(API_KEY)
    model = python.chat.load_model()

    data_source = datasource.PostgresDatasource("localhost", "postgres", "postgres", "password")

    @bot.message_handler(commands=["add_group"])
    def add_group_handler(message):
        group_name = message.text.replace("/add_group ", "", 1)
        language = "EN"

        data_source.insert_group_tag(group_name, language)

    @bot.message_handler(content_types=["text"])
    def message_handler(message):
        reply = model.answer(message.text)
        bot.send_message(message.chat.id, reply)

    def sigint_handler(sig, frame):
        data_source.close()
        bot.stop_polling()

    signal.signal(signal.SIGINT, sigint_handler)

    bot.polling()
