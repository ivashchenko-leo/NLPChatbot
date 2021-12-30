import telebot
import python.nn_model
import logging.config
from python import datasource
from python import commands
import signal
from python.message_parser import build_argparse


API_KEY = '5083139604:AAGcd0m6UhBkNmxIu78Nv2c53c0Q4lg8r14'
LANGUAGES = ['EN', 'RU']

DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "password"

logging.config.fileConfig("../logging.conf")


def train_model(language: str):
    data_source = datasource.PostgresDatasource(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)
    patterns = data_source.get_patterns(language)

    data_source.close()

    python.nn_model.train(patterns)


def run():
    logger = logging.getLogger()
    parser = build_argparse()

    bot = telebot.TeleBot(API_KEY)
    model = python.nn_model.load()

    data_source = datasource.PostgresDatasource(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)
    command_executor = commands.CommandExecutor(data_source)

    @bot.message_handler(commands=["exec"])
    def exec_handler(message):
        try:
            text = message.text.replace("/exec ", "", 1)
            args = parser.parse_args(text.split())
            language = "EN"

            if args.debug:
                logger.debug(args)

            if args.command == "add_group":
                command_executor.exec_add_group(" ".join(args.name), language)
            elif args.command == "add_pattern":
                command_executor.exec_add_pattern(" ".join(args.pattern), " ".join(args.group_tag), language)
            elif args.command == "add_response":
                command_executor.exec_add_response(" ".join(args.response), " ".join(args.group_tag), language)
        except Exception as ex:
            logger.exception(ex)

    @bot.message_handler(content_types=["text"])
    def message_handler(message):
        tag, prob = model.answer(message.text)
        language = "EN"
        if prob >= 0.75:
            response = data_source.get_response(tag, language)
        else:
            response = "I don't understand...."

        bot.send_message(message.chat.id, response)

    def sigint_handler(sig, frame):
        data_source.close()
        bot.stop_polling()

    signal.signal(signal.SIGINT, sigint_handler)

    bot.polling()
