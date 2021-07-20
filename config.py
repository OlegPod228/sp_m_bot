import json

import telebot
import sqlite3
import time
import qiwi_pay
import requests


# BOT
TOKEN = "1882373929:AAH2-5P43H0EELZ3IKXge9yBiXWprKa8uzg"
bot = telebot.TeleBot(TOKEN)

# for first start
status_subs = {}

day = time.strftime("%d")

# type spam (slow, average, fast)
type_spam = {}

# phone for spam
spam_to_number = {}

# quantity sended messages
quantity_send_message = {}

# for stop spam
stop_spam = {}

# Check subs on channel
def check_subs(id):
    if id == 779917069:
        return True
    try:
        return bot.get_chat_member(573845790, id)
    except:
        return False

# add user to db
def add_to_db(id):
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()

    ids = cursor.execute("SELECT `id` FROM `users`").fetchall()
    lis_id = []
    for x in ids:
        lis_id.append(x[0])

    if id not in lis_id:
        cursor.execute("INSERT INTO `users` VALUES (?,?,?,?,?)", (id, "", 0, 0, 0))
    conn.commit()

# update time users when he started spam
def upd_time(id):
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE `users` SET `last_start_spam` = ? WHERE `id` = ?", (time.strftime("%d.%m.20%y"), id))
    conn.commit()

# get statistic
def get_statistic(id):
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()
    data = cursor.execute("SELECT * FROM `users` WHERE `id` = ?", (id,)).fetchone()
    return data

# set quantity day using
def set_status(id, col_day):
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE `users` SET `VIP` = ? WHERE `id` = ?", (col_day, id))
    conn.commit()

# add message
def add_mess_db(id):
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()
    col = int(cursor.execute("SELECT `col_send_message` FROM `users` WHERE `id` = ?", (id,)).fetchone()[0])
    col += 1
    cursor.execute("UPDATE `users` SET `col_send_message` = ? WHERE `id` = ?", (col, id))
    conn.commit()


# del day
def del_day(id):
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()
    col = cursor.execute("SELECT `VIP` FROM `users` WHERE `id` = ?", (id,)).fetchone()[0]
    col -= 1
    if col <= 0:
        cursor.execute("UPDATE `users` SET `VIP` = ? WHERE `id` = ?", (0, id))
    else:
        cursor.execute("UPDATE `users` SET `VIP` = ? WHERE `id` = ?", (col, id))
    conn.commit()

# get status subscribe
def get_status_subs(id):
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()
    col = cursor.execute("SELECT `VIP` FROM `users` WHERE `id` = ?", (id,)).fetchone()[0]
    return True if col > 0 else False


def add_payment_db(id, code, month):
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO `premium` VALUES (?,?,?)", (id,month, code))
    conn.commit()

def check_pay():
    global  day
    while True:

        today = time.strftime("%d")

        conn = sqlite3.connect("user.db")
        cursor = conn.cursor()

        id_lis = cursor.execute("SELECT `id` FROM `users`").fetchall()

        if today != day:
            day = today
            for id in id_lis:
                del_day(id[0])

        data_list = cursor.execute("SELECT `id`, `code`, `day` FROM `premium`").fetchall()
        history_pay = qiwi_pay.payments_list()
        for data in data_list:
            if data[1] in history_pay:
                col = cursor.execute("SELECT `VIP` FROM `users` WHERE `id` = ?", (data[0],)).fetchone()[0]
                cursor.execute("UPDATE `users` SET `VIP` = ? WHERE `id` = ?", (col + data[2], data[0]))
                break


def new(url):

    session  = requests.Session()
    urls = "https://goo.su/run/convert"
    post = {'url': url,
            'alias': '',
            'password': '',
            'is_public': '1'}
    answ = session.post(urls, post)
    ret_url = json.loads(answ.content)
    return ret_url["short_url"].replace("\\", "")
