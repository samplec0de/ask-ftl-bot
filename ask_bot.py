import logging
from os import mkdir
from pathlib import Path

import telegram
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, Filters, MessageHandler, PicklePersistence
from yaml import safe_load

data = Path(__file__).parent / 'data'
if not data.exists():
    mkdir(data)
config = safe_load((data / "config.yml").read_text())
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
ASKING, TYPING_NEW_QUESTION = range(2)
main_reply_keyboard = [[config['buttons']['ask']], [config['buttons']['q_list']]]
main_reply_markup = ReplyKeyboardMarkup(main_reply_keyboard, one_time_keyboard=True, resize_keyboard=True)


def start(update: telegram.update.Update, context: telegram.ext.callbackcontext.CallbackContext):
    update.message.reply_text(config['messages']['start'], reply_markup=main_reply_markup)

    return ASKING


def ask(update: telegram.update.Update, context: telegram.ext.callbackcontext.CallbackContext):
    reply_keyboard = [[config['buttons']['cancel_ask']]]

    reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)

    update.message.reply_text(text=config['messages']['ask'], reply_markup=reply_markup)

    return TYPING_NEW_QUESTION


def q_list(update: telegram.update.Update, context: telegram.ext.callbackcontext.CallbackContext):
    reply_keyboard = [[config['buttons']['ask']]]

    reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)

    update.message.reply_text(text=config['messages']['q_list'], reply_markup=reply_markup)

    return ASKING


def user_question(update: telegram.update.Update, context: telegram.ext.callbackcontext.CallbackContext):
    update.message.reply_text(config['messages']['registered'], reply_markup=main_reply_markup)

    return ASKING


def cancel_ask(update: telegram.update.Update, context: telegram.ext.callbackcontext.CallbackContext):
    update.message.reply_text(config['messages']['canceled'], reply_markup=main_reply_markup)

    return ASKING


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    persistence = PicklePersistence(filename=str(data / 'persistence.pickle'))
    updater = Updater(config["token"], use_context=True, persistence=persistence)

    # updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_error_handler(error)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ASKING: [MessageHandler(Filters.regex(f'^{config["buttons"]["ask"]}$'), ask),
                     MessageHandler(Filters.regex(f'^{config["buttons"]["q_list"]}$'), q_list)],
            TYPING_NEW_QUESTION: [MessageHandler(Filters.regex(f'^({config["buttons"]["cancel_ask"]})$'), cancel_ask),
                                  MessageHandler(Filters.text, user_question)]
        },
        fallbacks=[],
        name="ask_conversation",
        persistent=True
    )

    updater.dispatcher.add_handler(conv_handler)

    # Запуск бота
    updater.start_polling()

    # Работать пока пользователь не нажмет Ctrl-C или процесс получит SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
