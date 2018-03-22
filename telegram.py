# basic telegram bot
# https://www.codementor.io/garethdwyer/building-a-telegram-bot-using-python-part-1-goi5fncay
# https://github.com/sixhobbits/python-telegram-tutorial/blob/master/part1/echobot.py

import json 
import requests
import time
import urllib
from DBhelper import DBHelper
import nltk.chat.iesha as iesha

# python3: urllib.parse.quote_plus
# python2: urllib.pathname2url

TOKEN = "556283248:AAGId4tLael98vEfBuJoW1DviS5Pv2bIi2Q" # don't put this in your repo! (put in config, then import config)
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
db = DBHelper()

"""
Useful commands:
link to bot: https://api.telegram.org/bot556283248:AAGId4tLael98vEfBuJoW1DviS5Pv2bIi2Q/getme
How to get the last text message:
print(get_last_chat_id_and_text(updates)[0])
"""


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def handle_updates(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            ids, texts = db.get_items()
            print("ids:", ids)
            if text in texts:
                #db.delete_item(text)
                ids, texts = db.get_items()
            else:
                db.add_item(text)
                items = db.get_items()
            print("texts:", texts)
            message = "\n".join(texts)
            send_message(message, chat)
        except KeyError:
            pass


def show_statistics(updates):
    for update in updates["result"]:
        stats = {}
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            ids, texts = db.get_items()
            for text in texts:
                words = text.split(" ")
                for word in words:
                    if word in stats:
                        stats[word] += 1
                    else:
                        stats[word] = 1
            message = ""
            for word in stats:
                message += word + ": " + str(stats[word]) + "\n"
            send_message(message, chat)
        except KeyError:
            pass


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def main():
    db.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            [text, chat_id] = get_last_chat_id_and_text(updates)
            if text == "!DropYourHottestMixtape" or text == "!stats":
                show_statistics(updates)
            else:
                handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
    # print(iesha.iesha_chat())
    # iesha.demo()

