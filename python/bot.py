import telebot
import python.chat
import logging.config
from python import datasource
from python import commands
import signal
from python.message_parser import build_argparse


API_KEY = '5083139604:AAGcd0m6UhBkNmxIu78Nv2c53c0Q4lg8r14'
LANGUAGES = ['EN', 'RU']


def run():
    logging.config.fileConfig("../logging.conf")
    logger = logging.getLogger()
    parser = build_argparse()

    bot = telebot.TeleBot(API_KEY)
    model = python.chat.load_model()

    data_source = datasource.PostgresDatasource("localhost", "postgres", "postgres", "password")
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
        reply = model.answer(message.text)
        bot.send_message(message.chat.id, reply)

    def sigint_handler(sig, frame):
        data_source.close()
        bot.stop_polling()

    signal.signal(signal.SIGINT, sigint_handler)

    bot.polling()
