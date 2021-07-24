from telebot import types


""" INLINE KEYBOARD """

# subs btn
sub_markup = types.InlineKeyboardMarkup()
sub_true_btn = types.InlineKeyboardButton("Я подписан", callback_data="true_sub")
sub_false_btn = types.InlineKeyboardButton("Подписаться", url="https://t.me/FireeGames")

sub_markup.add(sub_true_btn, sub_false_btn)

# speed send
speed_markup = types.InlineKeyboardMarkup(row_width=1)
slow_speed_btn = types.InlineKeyboardButton("Медленный", callback_data="slow")
average_speed_btn = types.InlineKeyboardButton("Средний", callback_data="average")
fast_speed_btn = types.InlineKeyboardButton("Быстрый", callback_data="fast")

speed_markup.add(slow_speed_btn,average_speed_btn,fast_speed_btn)

# start spam inline
start_spam_markup = types.InlineKeyboardMarkup(row_width=1)
start_spam_btn = types.InlineKeyboardButton("Начать спам", callback_data="start")
back_btn = types.InlineKeyboardButton("Назад", callback_data="back")

start_spam_markup.add(start_spam_btn, back_btn)

# buy subs
buy_subs = types.InlineKeyboardMarkup(row_width=1)
buy_149_btn = types.InlineKeyboardButton("Купить 149", callback_data="149_btn")
buy_249_btn = types.InlineKeyboardButton("Купить 249", callback_data="249_btn")
buy_349_btn = types.InlineKeyboardButton("Купить 349", callback_data="349_btn")

buy_subs.add(buy_149_btn, buy_249_btn, buy_349_btn)

# back inline
back_markup = types.InlineKeyboardMarkup()
back_inline_btn = types.InlineKeyboardButton("Назад", callback_data="back")

back_markup.add(back_inline_btn)

# buy btn
buy_markup = types.InlineKeyboardMarkup()
buy = types.InlineKeyboardButton("Купить", callback_data="buy")

buy_markup.add(buy)

# stop spam
stop_inline_markup = types.InlineKeyboardMarkup()
stop = types.InlineKeyboardButton("Завершить", callback_data="cancel")

stop_inline_markup.add(stop)

view_stat_markup = types.InlineKeyboardMarkup()
view_btn = types.InlineKeyboardButton("Статистика", callback_data="view_stat")
view_stat_markup.add(view_btn)

""" REPLY KEYBOARD """
# start spam
start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
start_spam_btn = types.KeyboardButton("Запустить спам")
statistic_btn = types.KeyboardButton("Статистика")
subs_btn = types.KeyboardButton("Подписка")

start_markup.add(start_spam_btn)
start_markup.add(statistic_btn, subs_btn)


# for admin
btn_for_admin = types.ReplyKeyboardMarkup(resize_keyboard=True)
admin_btn = types.KeyboardButton("Админ панель")

btn_for_admin.add(start_spam_btn)
btn_for_admin.add(statistic_btn, admin_btn)


# back btn
stop_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
stop = types.KeyboardButton("Назад")
stop_markup.add(stop)

# admin panel
admin_panel = types.ReplyKeyboardMarkup(resize_keyboard=True)
get_id = types.KeyboardButton("Выгрузить все ID")
send_post = types.KeyboardButton("Начать рассылку")
get_statistic_of_all_user = types.KeyboardButton("Статистика использования")


admin_panel.add(send_post)
admin_panel.add(get_id)
admin_panel.add(get_statistic_of_all_user)
admin_panel.add(stop)

# for post send
post_send = types.ReplyKeyboardMarkup(resize_keyboard=True)
send_post_with_photo = types.KeyboardButton("Пост с фото")
send_post_with_video = types.KeyboardButton("Пост с видео")
send_post_with_gif = types.KeyboardButton("Пост с гифкой")
send_post_with_sticker = types.KeyboardButton("Пост со стикеором")
send_post_without_photo = types.KeyboardButton("Пост без фото")
forward_post = types.KeyboardButton("Переслать пост")
post_send.add(send_post_with_photo,send_post_without_photo)
post_send.add(send_post_with_video, send_post_with_gif)
post_send.add(forward_post)
post_send.add(stop)