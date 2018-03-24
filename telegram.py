# basic telegram bot
# https://www.codementor.io/garethdwyer/building-a-telegram-bot-using-python-part-1-goi5fncay
# https://github.com/sixhobbits/python-telegram-tutorial/blob/master/part1/echobot.py

import json
import requests
import time
import urllib
import random
from DBhelper import DBHelper
import numpy as np
import nltk.chat.iesha as iesha
TOKEN = "556283248:AAGId4tLael98vEfBuJoW1DviS5Pv2bIi2Q" # don't put this in your repo! (put in config, then import config)
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
db = DBHelper()

"""
Useful commands:
link to bot: https://api.telegram.org/bot556283248:AAGId4tLael98vEfBuJoW1DviS5Pv2bIi2Q/getme
How to get the last text message:
print(get_last_chat_id_and_text(updates)[0])
Useful information:
The Dictionary has 268973 entries.
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
            # make the text all capital letters, bc in our db they are all capital
            text = text.upper()
            # we are only interested in the last word:
            text = text.split(" ")[-1]
            print("Text:", text)
            chat = update["message"]["chat"]["id"]
            words, phonemes = db.get_items("rhymes")

            # if we have a phoneme composition of the word, use that for further work. Else, send an error message
            if text in words:
                print("thinking")
                ph = phonemes[words.index(text)].split(" ")
                # in ph are the phonemes of the input word, now we want to find a word with similar phonemes:
                best_index = 0
                best_score = 1
                rhymes = {}
                for index, word in enumerate(words):
                    ph2 = phonemes[index].split(" ")
                    score = 1
                    minimum = min(len(ph), len(ph2))
                    for i in range(1, 1+minimum):
                        if ph[-i] == ph2[-i]:
                            score *= minimum - i + 1
                    if score >= 2:
                        rhymes[word] = score

                    # print(best_score, best_index)
                max_score = max(rhymes.values())
                rhymes_string = [word for word in rhymes if rhymes[word] == max_score]
                # look if some word in rhymes_string matches the vocabulary of Kanye
                row, kanye_words = db.get_items("kanye")
                kanye_words = np.random.permutation(kanye_words)
                target_word = ""
                for kanye_word in kanye_words:
                    if kanye_word.upper() in rhymes_string:
                        kanye_lyrics = open("KanyeWest.txt", 'r', encoding='UTF-8').readlines()
                        row_index = db.get_index("kanye", kanye_word)[0]
                        message = kanye_lyrics[row_index : row_index+5]
                        print(message)
                        send_message("".join(message), chat)
                        return
                out = []
                for i in range(5):
                    out.append(rhymes_string[random.randint(0, len(rhymes_string)-1)])

                send_message("\n".join(out), chat)

            else:
                print("not in db")
                message = "Yo, what doz that mean?"
                send_message(message, chat)
                return

        except KeyError:
            pass


def show_statistics(updates):
    for update in updates["result"]:
        stats = {}
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            ids, texts = db.get_items()
            for text in texts[0:10]:
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