import time

import requests

import qiwi_pay
import telebot
import config
import button

from telebot.util import async_dec
from telebot import types
from SMS.main import SMS_ATTACK

bot = telebot.TeleBot(config.TOKEN)


# message handlers
@async_dec()
@bot.message_handler(content_types=["text"])
def handler(message):

    if message.text == "Назад":
        bot.clear_step_handler_by_chat_id(message.chat.id)
        if message.from_user.id != 573845790 or message.from_user.id != 779917069:
            bot.send_message(message.chat.id, "Назад", reply_markup=button.btn_for_admin)
        else:
            bot.send_message(message.chat.id, "Назад", reply_markup=button.start_markup)

    # start spam
    if message.text == "Запустить спам":
        bot.send_message(message.chat.id, 'Введите номер телефона без (+) на который будет отправлен спам. \n\nПример: <code>79993433765</code> ', parse_mode="HTML", reply_markup=button.stop_markup)
        bot.register_next_step_handler(message, add_phone_number_for_spam)

    # first start bot
    if message.text == "/start":
        config.status_subs[message.from_user.id] = 0
        text = "Привет [{}](https://t.me/{}), меня зовут [Darpix](https://t.me/Darpixbot)\n\nПодпишись на канал чтобы начать пользоваться ботом\.".format(
            message.from_user.first_name, message.from_user.username)
        bot.send_message(message.chat.id, text, reply_markup=button.sub_markup, parse_mode="MarkdownV2")


    # statistic users
    if message.text == "Статистика":
        data = config.get_statistic(message.chat.id)
        if data[3] == 0:
            text = "Статистика пользователя.\n<code>Aктуальная дата {}</code>\nid пользователя: <code>{}</code>\nПодписка: <code>Отсутствует</code>\nCмс отправленно: <code>{}</code>".format(data[1], data[0],data[4])
        else:
            text = "Статистика пользователя.\n<code>Aктуальная дата {}</code>\nid пользователя: <code>{}</code>\nПодписка: <code>действительна {} дня|день</code>\nCмс отправленно: <code>{}</code>".format(data[1],data[0], data[3], data[4])

        bot.send_message(message.chat.id, text, reply_markup=button.stop_markup, parse_mode="HTML")

    if message.text == "Подписка":
        text = "Подписка [Darpix Devil SMS](https://t.me/Darpixbot)\.\n\nПодписка дает вам безраничные возможности использования Darpix\.\n\n1 Максимальная скорость спама лучше вы не найдете\.\n2 Безграничное время использования\.\n3 Возможность выбора режимов Медленный \- Cредний \- Быстрый\n4 Анонимность при испоьзование никто не узнает кто запустил спам\n5 Стабильная работы 24\/7 бот регулярно  обновляется\."
        bot.send_message(message.chat.id, text = text,reply_markup=button.buy_markup, parse_mode="MarkdownV2")

    if message.text == "Админ панель":
        bot.send_message(message.chat.id, "Админ панель", reply_markup=button.admin_panel)

    if message.text == "Начать рассылку":
        config.col_btn_on_post = {}
        config.text_for_post = ""
        bot.send_message(message.chat.id, "Отправьте фото")
        bot.register_next_step_handler(message, _send_photo)

    if message.text == "Выгрузить все ID":
        config.save_to_excel()
        bot.send_document(message.chat.id, open("send_id.xlsx", "rb"))

# set number phone for spam
@async_dec()
def add_phone_number_for_spam(message):
    if message.text == "Назад":
        bot.clear_step_handler_by_chat_id(message.chat.id)
        if message.from_user.id != 573845790 or message.from_user.id != 779917069:
            bot.send_message(message.chat.id, "Назад", reply_markup=button.btn_for_admin)
        else:
            bot.send_message(message.chat.id, "Назад", reply_markup=button.start_markup)
    else:
        if (len(message.text) == 12 and message.text[0] == "3") or (len(message.text) == 11 and message.text[0] == "7"):
            config.spam_to_number[message.from_user.id] = message.text.replace("+", "")
            text = "Начать спам на номер. <code>({})</code> \n\nВ бесплатной версии доступен только медленный режим!\n\nВыберите режим спама.\n\nМедленный - <code>до 20 смс в минуту</code>\n\nСредний - <code>до 40 смс в минуту</code>\n\nБыстрый - <code>до 60 смс в минуту</code>".format(message.text.replace("+", ""))
            bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=button.speed_markup)
        else:
            bot.send_message(message.chat.id,
                             'Введите номер телефона без (+) на который будет отправлен спам. \n\nПример: <code>79993433765</code> ',
                             parse_mode="HTML", reply_markup=button.stop_markup)
            bot.register_next_step_handler(message, add_phone_number_for_spam)

def _send_photo(message):
    try:
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)

        with open("send_image.png", 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.send_message(message.chat.id, "Отправьте текст поста")
        bot.register_next_step_handler(message, _send_text)
    except:
        bot.send_message(message.chat.id, "Что-то пошло не так...")

def _send_text(message):
    if message.text == "Назад":
        bot.clear_step_handler_by_chat_id(message.chat.id)
        if message.from_user.id != 573845790 or message.from_user.id != 779917069:
            bot.send_message(message.chat.id, "Назад", reply_markup=button.btn_for_admin)
        else:
            bot.send_message(message.chat.id, "Назад", reply_markup=button.start_markup)
    else:
        config.text_for_post = message.text

        send_markup = types.InlineKeyboardMarkup(row_width=1)
        send_btn = types.InlineKeyboardButton("Отправить", callback_data="send_post")
        add_btn = types.InlineKeyboardButton("Добавить кнопку", callback_data="add_btn")
        send_markup.add(send_btn,add_btn)

        bot.send_photo(message.chat.id, open("send_image.png", "rb").read(), caption=message.text, reply_markup=send_markup)

def add_btn(message):
    try:
        if len(config.col_btn_on_post.keys()) == 0:
            config.col_btn_on_post[message.text.split(" ")[0]] = message.text.split(" ")[1]
            send_markup = types.InlineKeyboardMarkup(row_width=1)
            send_btn = types.InlineKeyboardButton("Отправить", callback_data="send_post")
            url1 = types.InlineKeyboardButton(message.text.split(" ")[0], url=message.text.split(" ")[1])
            add_btn = types.InlineKeyboardButton("Добавить кнопку", callback_data="add_btn")
            send_markup.add(url1,send_btn, add_btn)

            bot.send_photo(message.chat.id, open("send_image.png", "rb").read(), caption=config.text_for_post, reply_markup=send_markup)

        elif len(config.col_btn_on_post.keys()) == 1:
            send_markup = types.InlineKeyboardMarkup(row_width=1)
            send_btn = types.InlineKeyboardButton("Отправить", callback_data="send_post")
            data = config.col_btn_on_post.keys()
            for x in data:
                url1 = types.InlineKeyboardButton(x, url=config.col_btn_on_post[x])
            url2 = types.InlineKeyboardButton(message.text.split(" ")[0], url=message.text.split(" ")[1])
            send_markup.add(url1, url2, send_btn)
            config.col_btn_on_post[message.text.split(" ")[0]] = message.text.split(" ")[1]
            bot.send_photo(message.chat.id, open("send_image.png", "rb").read(), caption=config.text_for_post,
                           reply_markup=send_markup)
    except:
        bot.send_message(message.chat.id, "Что-то пошло не так...")

# Call Handler
@async_dec()
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        # call subs
        if call.data == "true_sub":

            # if user subscribe on channel
            if config.check_subs(call.from_user.id):
                if call.from_user.id != 573845790 or call.from_user.id != 779917069:
                    text = "Привет [{}](https://t.me/{}), меня зовут [Darpix](https://t.me/Darpixbot)\n\nСпасибо за подписку теперь вы можете использовать бота\.".format(
                        call.from_user.first_name, call.from_user.username)
                    bot.edit_message_text(text=text, message_id=call.message.message_id, chat_id=call.message.chat.id,
                                          parse_mode="MarkdownV2")
                    bot.send_message(call.message.chat.id, "Бот разблокирован", reply_markup=button.btn_for_admin)
                    config.add_to_db(call.from_user.id, call.from_user.username)
                else:
                    text = "Привет [{}](https://t.me/{}), меня зовут [Darpix](https://t.me/Darpixbot)\n\nСпасибо за подписку теперь вы можете использовать бота\.".format(
                        call.from_user.first_name, call.from_user.username)
                    bot.edit_message_text(text=text, message_id=call.message.message_id, chat_id=call.message.chat.id,
                                          parse_mode="MarkdownV2")
                    bot.send_message(call.message.chat.id, "Бот разблокирован", reply_markup=button.start_markup)
                    config.add_to_db(call.from_user.id, call.from_user.username)

            # if user not subscribe on channel
            else:
                if config.status_subs[call.from_user.id] == 1:
                    text = "Привет [{}](https://t.me/{}), меня зовут [Darpix](https://t.me/Darpixbot)\n\nПослушай я тоже хочу кушать\!".format(
                        call.from_user.first_name, call.from_user.username)
                    bot.edit_message_text(text=text, message_id=call.message.message_id, chat_id=call.message.chat.id,
                                          reply_markup=button.sub_markup, parse_mode="MarkdownV2")
                    config.status_subs[call.from_user.id] = 2

                elif config.status_subs[call.from_user.id] == 0:
                    text = "Привет [{}](https://t.me/{}), меня зовут [Darpix](https://t.me/Darpixbot)\n\nТы еще не подписан я все вижу\!".format(
                        call.from_user.first_name, call.from_user.username)
                    bot.edit_message_text(text=text, message_id=call.message.message_id, chat_id=call.message.chat.id,
                                          reply_markup=button.sub_markup, parse_mode="MarkdownV2")
                    config.status_subs[call.from_user.id] = 1

                else:
                    text = "Привет [{}](https://t.me/{}), меня зовут [Darpix](https://t.me/Darpixbot)\n\nПодпишись на канал чтобы начать пользоваться ботом\.".format(
                        call.from_user.first_name, call.from_user.username)
                    bot.edit_message_text(text=text, message_id=call.message.message_id, chat_id=call.message.chat.id,
                                          reply_markup=button.sub_markup, parse_mode="MarkdownV2")

        # slow speed
        if call.data == "slow":
            text = "Начать спам на номер\n<code>{}</code>\n\nРежим: <code>Медленный</code>\n\nСпам будет длится не более 10 минут.\n\nЧтобы увеличить длительность и мощьность приобретите <code>подписку</code>".format(config.spam_to_number[call.from_user.id])
            bot.edit_message_text(chat_id=call.message.chat.id, text = text, message_id=call.message.message_id, reply_markup=button.start_spam_markup, parse_mode="HTML")
            config.type_spam[call.from_user.id] = 0

        # average speed
        if call.data == "average":
            if config.get_status_subs(call.from_user.id):
                text = "Начать спам на номер\n<code>{}</code>\n\nРежим: <code>Средний</code>\n\nСпам будет длится неограниченное время.".format(config.spam_to_number[call.from_user.id])
                bot.edit_message_text(chat_id=call.message.chat.id, text=text, message_id=call.message.message_id,
                                      reply_markup=button.start_spam_markup, parse_mode="HTML")
                config.type_spam[call.from_user.id] = 1
            else:
                text = "Нету доступа... \nКупите подписку для открытия данной скорости"
                bot.edit_message_text(chat_id=call.message.chat.id, text=text, message_id=call.message.message_id,
                                      reply_markup=button.back_markup)

        # fast speed
        if call.data == "fast":
            if config.get_status_subs(call.from_user.id):
                text = "Начать спам на номер\n<code>{}</code>\n\nРежим: <code>Быстрый</code>\n\nСпам будет длится неограниченное время.".format(config.spam_to_number[call.from_user.id])
                bot.edit_message_text(chat_id=call.message.chat.id, text=text, message_id=call.message.message_id,
                                      reply_markup=button.start_spam_markup, parse_mode="HTML")
                config.type_spam[call.from_user.id] = 2
            else:
                text = "Нету доступа... \nКупите подписку для открытия данной скорости"
                bot.edit_message_text(chat_id=call.message.chat.id, text=text, message_id=call.message.message_id,
                                      reply_markup=button.back_markup)

        # start spam
        if call.data == "start":
            # slow speed
            if config.type_spam[call.from_user.id] == 0:
                text = "Спам начат.\n\nДата <code>{}</code>\n\nНомер <code>{}</code>\n\nРежим  <code>Медленный</code>".format(time.strftime("%d.%m.20%y"), config.spam_to_number[call.from_user.id])
                bot.edit_message_text(chat_id=call.message.chat.id, text=text, message_id=call.message.message_id,
                                      reply_markup=button.stop_inline_markup, parse_mode="HTML")
                config.quantity_send_message[call.from_user.id] = 0
                config.stop_spam[call.from_user.id] = False
                config.upd_time(call.from_user.id)
                SMS_ATTACK(call.from_user.id, config.spam_to_number[call.from_user.id])
            # average speed
            if config.type_spam[call.from_user.id] == 1:
                config.quantity_send_message[call.from_user.id] = 0
                text = "Спам начат.\n\nДата <code>{}</code>\n\nНомер <code>{}</code>\n\nРежим  <code>Средний</code>".format(
                    time.strftime("%d.%m.20%y"), config.spam_to_number[call.from_user.id])
                bot.edit_message_text(chat_id=call.message.chat.id, text=text, message_id=call.message.message_id,
                                      reply_markup=button.stop_inline_markup, parse_mode="HTML")
                config.stop_spam[call.from_user.id] = False
                config.upd_time(call.from_user.id)
                SMS_ATTACK(call.from_user.id, config.spam_to_number[call.from_user.id])

            # fast speed
            if config.type_spam[call.from_user.id] == 2:
                config.quantity_send_message[call.from_user.id] = 0
                text = "Спам начат.\n\nДата <code>{}</code>\n\nНомер <code>{}</code>\n\nРежим  <code>Быстрый</code>".format(
                    time.strftime("%d.%m.20%y"), config.spam_to_number[call.from_user.id])
                bot.edit_message_text(chat_id=call.message.chat.id, text=text, message_id=call.message.message_id,
                                      reply_markup=button.stop_inline_markup, parse_mode="HTML")
                config.stop_spam[call.from_user.id] = False
                config.upd_time(call.from_user.id)
                SMS_ATTACK(call.from_user.id, config.spam_to_number[call.from_user.id])

        # cancel spam
        if call.data == "back":
            text = "Начать спам на номер. <code>({})</code> \n\nВ бесплатной версии доступен только медленный режим!\n\nВыберите режим спама.\n\nМедленный - <code>до 20 смс в минуту</code>\n\nСредний - <code>до 40 смс в минуту</code>\n\nБыстрый - <code>до 60 смс в минуту</code>".format(config.spam_to_number[call.from_user.id])
            bot.edit_message_text(chat_id=call.message.chat.id, text=text, message_id=call.message.message_id,
                                  reply_markup=button.speed_markup, parse_mode="HTML")

        # buy
        if call.data == "buy":
            text = "Подписка [Darpix Devil SMS](https://t.me/Darpixbot)\.\n\nПодписка дает вам безраничные возможности использования Darpix\.\n\n1 Максимальная скорость спама лучше вы не найдете\.\n2 Безграничное время использования\.\n3 Возможность выбора режимов Медленный \- Cредний \- Быстрый\n4 Анонимность при испоьзование никто не узнает кто запустил спам\n5 Стабильная работы 24\/7 бот регулярно  обновляется\."
            bot.edit_message_text(chat_id=call.message.chat.id, message_id= call.message.message_id, text = text, reply_markup=None,parse_mode="MarkdownV2")

            # for payment
            key = "48e7qUxn9T7RyYE1MVZswX1FRSbE6iyCj2gCRwwF3Dnh5XrasNTx3BGPiMsyXQFNKQhvukniQG8RTVhYm3iPv76mVvVLZ4eiRLXshG7ndEvAGfTMFnxyMPJQsj7uwM4tPU9xPhqGsP9AeTdQ4r6CRT3ygNXg7Zq9os4sPd1uDv39zQDuzKPvVVA5yMY1n"
            random_key = qiwi_pay.generate_random_commment()
            url_149 = f"https://oplata.qiwi.com/create?publicKey={key}&amount=149&comment={random_key}"
            url_249 = f"https://oplata.qiwi.com/create?publicKey={key}&amount=249&comment={random_key}"
            url_349 = f"https://oplata.qiwi.com/create?publicKey={key}&amount=349&comment={random_key}"

            # Keyboard
            payment = types.InlineKeyboardMarkup(row_width=1)
            pay_149 = types.InlineKeyboardButton("Купить 149", callback_data="149_btn")
            pay_249 = types.InlineKeyboardButton("Купить 249", callback_data="249_btn")
            pay_349 = types.InlineKeyboardButton("Купить 349", callback_data="349_btn")
            payment.add(pay_149, pay_249, pay_349)

            text = "Стоимость подписки [Darpix Devill SMS](https://t.me/Darpixbot)\n\n149 \- подписка на 1 месяц \n249 \- подписка на 2 месяца\n349 \- подписка на 3 месяца\n\nВыберите подходящий тариф и оплатите по ссылке ниже\, подписка начинает действовать моментально с момента оплаты\.\n\n[Если у вас возникнут какие\-либо проблемы пишите сюда \- @DarpixSupport](https://t.me/DarpixSupport)"
            bot.send_message(call.message.chat.id, text=text, reply_markup=payment, parse_mode="MarkdownV2")

        # stop spam
        if call.data == "cancel":
            config.stop_spam[call.from_user.id] = True
            if config.type_spam[call.from_user.id] == 0:
                text = "Спам начат.\n\nДата <code>{}</code>\n\nНомер <code>{}</code>\n\nРежим  <code>Медленный</code>".format(
                    time.strftime("%d.%m.20%y"), config.spam_to_number[call.from_user.id])
            if config.type_spam[call.from_user.id] == 1:
                text = "Спам начат.\n\nДата <code>{}</code>\n\nНомер <code>{}</code>\n\nРежим  <code>Средний</code>".format(
                    time.strftime("%d.%m.20%y"), config.spam_to_number[call.from_user.id])
            if config.type_spam[call.from_user.id] == 2:
                text = "Спам начат.\n\nДата <code>{}</code>\n\nНомер <code>{}</code>\n\nРежим  <code>Быстрый</code>".format(
                    time.strftime("%d.%m.20%y"), config.spam_to_number[call.from_user.id])
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = text, reply_markup=None, parse_mode="HTML")
            text = "Спам завершен.\n\nДата <code>{}</code>\n\nНомер - <code>{}</code>\n\nОтправленно СМС - <code>{}</code>".format(time.strftime("%d.%m.20%y"), config.spam_to_number[call.from_user.id], config.quantity_send_message[call.from_user.id])
            bot.send_message(call.message.chat.id, text, parse_mode="HTML")


        """             BUY SUBS                """

        # 149 rub
        if call.data == "149_btn":
            text = "Оплатить доступ на 1 (31 день) месяц за 149 руб."

            key = "48e7qUxn9T7RyYE1MVZswX1FRSbE6iyCj2gCRwwF3Dnh5XrasNTx3BGPiMsyXQFNKQhvukniQG8RTVhYm3iPv76mVvVLZ4eiRLXshG7ndEvAGfTMFnxyMPJQsj7uwM4tPU9xPhqGsP9AeTdQ4r6CRT3ygNXg7Zq9os4sPd1uDv39zQDuzKPvVVA5yMY1n"
            random_key = qiwi_pay.generate_random_commment()
            url_149 = config.new(f"https://oplata.qiwi.com/create?publicKey={key}&amount=149&comment={random_key}")

            # accept payment
            payment = types.InlineKeyboardMarkup()
            payment_btn = types.InlineKeyboardButton("Оплатить", url=url_149)
            payment.add(payment_btn)
            config.add_payment_db(call.from_user.id, random_key, 31)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text,
                                  reply_markup=payment)

        # 249 rub
        if call.data == "249_btn":
            text = "Оплатить доступ на 2 (62 дня) месяцa за 249 руб."

            key = "48e7qUxn9T7RyYE1MVZswX1FRSbE6iyCj2gCRwwF3Dnh5XrasNTx3BGPiMsyXQFNKQhvukniQG8RTVhYm3iPv76mVvVLZ4eiRLXshG7ndEvAGfTMFnxyMPJQsj7uwM4tPU9xPhqGsP9AeTdQ4r6CRT3ygNXg7Zq9os4sPd1uDv39zQDuzKPvVVA5yMY1n"
            random_key = qiwi_pay.generate_random_commment()
            url_249 = config.new(f"https://oplata.qiwi.com/create?publicKey={key}&amount=249&comment={random_key}")

            # accept payment
            payment = types.InlineKeyboardMarkup()
            payment_btn = types.InlineKeyboardButton("Оплатить", url=url_249)
            payment.add(payment_btn)
            config.add_payment_db(call.from_user.id, random_key, 62)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text,
                                  reply_markup=payment)

        # 349 rub
        if call.data == "349_btn":
            text = "Оплатить доступ на 3 (93 дня) месяцa за 349 руб."

            key = "48e7qUxn9T7RyYE1MVZswX1FRSbE6iyCj2gCRwwF3Dnh5XrasNTx3BGPiMsyXQFNKQhvukniQG8RTVhYm3iPv76mVvVLZ4eiRLXshG7ndEvAGfTMFnxyMPJQsj7uwM4tPU9xPhqGsP9AeTdQ4r6CRT3ygNXg7Zq9os4sPd1uDv39zQDuzKPvVVA5yMY1n"
            random_key = qiwi_pay.generate_random_commment()
            url_349 = config.new(f"https://oplata.qiwi.com/create?publicKey={key}&amount=349&comment={random_key}")

            # accept payment
            payment = types.InlineKeyboardMarkup()
            payment_btn = types.InlineKeyboardButton("Оплатить", url=url_349)
            payment.add(payment_btn)
            config.add_payment_db(call.from_user.id, random_key, 93)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text,
                                  reply_markup=payment)


        """             SEND POST               """

        if call.data == "send_post":
            all_id = config.get_all_id()

            last_btn_name = ""
            last_btn_url = ""
            markup = types.InlineKeyboardMarkup(row_width=1)
            if len(config.col_btn_on_post.keys()) == 1:
                for x in config.col_btn_on_post.keys():
                    last_btn_name = x
                    last_btn_url = config.col_btn_on_post[x]
                    url1 = types.InlineKeyboardButton(x,url=config.col_btn_on_post[x])
                    markup.add(url1)

            if len(config.col_btn_on_post.keys()) == 2:
                for x in config.col_btn_on_post.keys():
                    if x == last_btn_name:
                        continue
                    url2 = types.InlineKeyboardButton(x, url=config.col_btn_on_post[x])
                    markup.add(url2)

            for id in all_id:
                try:
                    bot.send_photo(id, open("send_image.png", "rb").read(), caption=config.text_for_post, reply_markup=markup)
                except:
                    bot.send_photo(id, open("send_image.png", "rb").read(), caption=config.text_for_post)

        if call.data == "add_btn":
            bot.send_message(call.message.chat.id, "Текст и ссылку разделяя их пробелом \n[test www.test.com]")
            bot.register_next_step_handler(call.message, add_btn)

    except Exception as e:
        print(repr(e))


# to loop bot
bot.polling(none_stop=True)