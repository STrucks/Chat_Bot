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
from config import TOKEN

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


def clean_word(word):
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    new_word = ""
    for c in word:
        if c in letters:
            new_word += c
    return new_word


def simple_rhyme(updates, word_list):
    for update in updates["result"]:
        try:
            chat = update["message"]["chat"]["id"]
            message = ""
            for word in word_list:
                word = word.upper()
                word = clean_word(word)
                rhyme_words, phonemes = db.get_items("rhymes")
                if word in rhyme_words:
                    print("thinking")
                    ph = phonemes[rhyme_words.index(word)].split(" ")
                    rhymes = {}
                    for index, rhyme in enumerate(rhyme_words):
                        ph2 = phonemes[index].split(" ")
                        score = 1
                        minimum = min(len(ph), len(ph2))
                        for i in range(1, 1 + minimum):
                            if ph[-i] == ph2[-i]:
                                score *= minimum - i + 1
                        if score >= 2:
                            rhymes[rhyme] = score
                            # print(best_score, best_index)
                    max_score = max(rhymes.values())
                    rhymes_string = [word for word in rhymes if rhymes[word] == max_score]
                    message += rhymes_string[random.randint(0,len(rhymes_string)-1)] + " "
                else:
                    message = "Yo what does dis mean? "
            print(message)
            send_message(message.lower(), chat)

        except KeyError:
            pass


def handle_updates(updates, rapper = "kanye"):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            # make the text all capital letters, bc in our db they are all capital
            text = text.upper()
            # we are only interested in the last word:
            text = text.split(" ")[-1]
            # clean that word (i.e. remove non letters)
            text = clean_word(text)
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
                # look if some word in rhymes_string matches the vocabulary of the rapper
                if rapper == "kanye":
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
                    # for i in range(5):
                    #     out.append(rhymes_string[random.randint(0, len(rhymes_string)-1)])

#                     send_message("\n".join(out), chat)
                elif rapper == "eminem":
                    row, eminem_words = db.get_items("eminem")
                    eminem_words = np.random.permutation(eminem_words)
                    target_word = ""
                    for eminem_word in eminem_words:
                        if eminem_word.upper() in rhymes_string:
                            eminem_lyrics = open("Eminem.txt", 'r', encoding='ISO-8859-1').readlines()
                            row_index = db.get_index("eminem", eminem_word)[0]
                            message = eminem_lyrics[row_index: row_index + 5]
                            print(message)
                            send_message("".join(message), chat)
                            return

                send_message(rapper + " does not rhyme to that word.", chat)
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
    if "text" not in updates["result"][last_update]["message"]:
        return ("", 0)
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
    rapper = "kanye"
    start = True
    while True:
        updates = get_updates(last_update_id)

        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            [text, chat_id] = get_last_chat_id_and_text(updates)
            if start:
                msg = "Yo, my name is Rap God. Im a Chat Bot.\nI am the best, let's give it a test!\nYou wanna know what I can do, type !help and I can tell you!"
                send_message(msg, chat_id)
                start = False
            elif text == "!help":
                msg = "I can immitate rappers. Write somethning and I will rap to that.\n\n!Kanye makes me immitate Kanye West\n!Eminem makes me immitate Eminem\n\nIf you just want to know a rhyme, type \n\n !rhyme *word* and I will give you a rhyme to every word!\n\nType !Goodbye to let me know you are leaving."
                send_message(msg, chat_id)
            elif text == "!Goodbye":
                msg = "Smell ya later, alligator!"
                send_message(msg, chat_id)
                return
            elif text == "!Eminem":
                rapper = "eminem"
            elif text == "!Kanye":
                rapper = "kanye"
            elif "!rhyme" in text:
                words = text.split(" ")
                words.remove("!rhyme")
                simple_rhyme(updates, words)
            else:
                handle_updates(updates, rapper)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
    # print(iesha.iesha_chat())
    # iesha.demo()