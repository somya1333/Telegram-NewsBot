import logging
from flask import Flask, request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
from telegram import Bot, Update
from util import get_reply, fetch_news
from googlesearch import search

# logging the details
# logging module is used so that all the messages including the errors are shown in pre-defined systematic order
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' , level=logging.INFO)
logger=logging.getLogger(__name__)

bot_token = '1141938313:AAG9japKMvDoke6i5VFsD4mvXbvOLy61_ps'

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
    # msg = update.message.text
    reply = f"Ok! This is help desk"
    bot.send_message(chat_id = update.message.chat_id, text=reply)

def replytext(bot, update):
    intent, reply = get_reply(update.message.text, update.message.chat_id)
    if intent=="news.search":
        # replytext="ok"
        bot.send_message(chat_id = update.message.chat_id, text=reply)
        # for j in search(update.message.text, tld="co.in", num=3, stop=3, pause=2): 
        #     bot.send_message(chat_id = update.message.chat_id, text=j)
        # reply_articles = fetch_news(reply)
        # for articles in reply_articles:
        #     bot.send_message(chat_id = update.message.chat_id, text=articles['link'])
    else:
        bot.send_message(chat_id = update.message.chat_id, text=reply)

def copysticker(bot, update):
    # msg = update.message.sticker.file_id
    bot.send_sticker(chat_id = update.message.chat_id, sticker=update.message.sticker.file_id)

def error(bot, update):
    logger.error("Update '%s' caused error '%s'",update,update.error)

# any update is recieved by the updater
# updates are handeled by the dispatcher
# def main():

    # updater.start_polling() 
    # logger.info('Started Polling...')
    # updater.idle()

if __name__=='__main__':
    bot = Bot(bot_token)
    bot.set_webhook("https://04d40161d5d2.ngrok.io/" + bot_token)

    dp = Dispatcher(bot, None)
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('help',_help))
    dp.add_handler(MessageHandler(Filters.text,replytext))
    dp.add_handler(MessageHandler(Filters.sticker,copysticker))
    dp.add_error_handler(error)
    app.run(port=8443)