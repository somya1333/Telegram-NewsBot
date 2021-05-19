import logging
from flask import Flask, request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
from telegram import Bot, Update
from util import get_reply, fetch_news
from googlesearch import search

# logging the details
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' , level=logging.INFO)
logger=logging.getLogger(__name__)

bot_token = 'Enter your bot token here'

app=Flask('__name__')

# def index():
#     print("HELLO")

@app.route(f'/{bot_token}',methods=['GET','POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dp.process_update(update)
    return 'ok'

def start(bot, update):
    author = update.message.from_user.first_name
    # msg = update.message.text
    reply = f"Hi {author}"
    bot.send_message(chat_id=update.message.chat_id, text=reply)

def _help(bot, update):
    author=update.message.from_user.first_name
    reply = f"I will help you {author}"
    bot.send_message(chat_id = update.message.chat_id, text=reply)

def replytext(bot, update):
    intent, reply = get_reply(update.message.text, update.message.chat_id)
    if intent=='get_news':
        articles=fetch_news(reply)
        for  article in articles:
            bot.send_message(chat_id=update.message.chat_id,text=article['link'])
    else:
        bot.send_message(chat_id=update.message.chat_id,text=reply)

def copysticker(bot, update):
    # msg = update.message.sticker.file_id
    bot.send_sticker(chat_id = update.message.chat_id, sticker=update.message.sticker.file_id)

def error(bot, update):
    logger.error("Update '%s' caused error '%s'",update,update.error)


if __name__=='__main__':
    bot = Bot(bot_token)
    bot.set_webhook("Enter the publically accessible URL here" + bot_token)

    dp = Dispatcher(bot, None)
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('help',_help))
    dp.add_handler(MessageHandler(Filters.text,replytext))
    dp.add_handler(MessageHandler(Filters.sticker,copysticker))
    dp.add_error_handler(error)
    app.run(port=8443)
