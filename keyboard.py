from telebot import types
import config
import functions as func

main_menu_btn = [
    'Mеню'
]


def bomber_start_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text='🧨 Выключить бомбер', callback_data=f'bomb_off'),
    )
    return markup


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    row_keyboard = [{'text': 'Меню'}]
    buttons = func.get_reklama_button()
    this_row = 0
    for button in buttons:
        if len(row_keyboard) == 3:
            this_row = 1
            markup.keyboard.append(row_keyboard)
            row_keyboard = []
        row_keyboard.append({'text': button[1]})
    if this_row == 0:
        markup.keyboard.append(row_keyboard)
    elif row_keyboard != 3 and row_keyboard != 0:
        markup.keyboard.append(row_keyboard)
    return markup


def delete_message():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(text='❌ Понял', callback_data='delete_message'))
    return markup


def how_to_delete():
    markup = types.InlineKeyboardMarkup(row_width=3)
    row_keyboard = [types.InlineKeyboardButton('Меню', callback_data='test')]
    buttons = func.get_reklama_button()
    this_row = 0
    for button in buttons:
        if len(row_keyboard) == 3:
            this_row = 1
            markup.keyboard.append(row_keyboard)
            row_keyboard = []
        row_keyboard.append(types.InlineKeyboardButton(button[1], callback_data='del_button=' + button[1]))
    if this_row == 0:
        markup.keyboard.append(row_keyboard)
    elif row_keyboard != 3 and row_keyboard != 0:
        markup.keyboard.append(row_keyboard)
    return markup


def menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text='📲 Бомбить номер', callback_data=f'bomb_started'),
    )
    markup.add(
        types.InlineKeyboardButton(text='🌍 Страна Бомбежки', callback_data='country'),
        types.InlineKeyboardButton(text='⏱ Активные Бомбежки ', callback_data='active_bomb'),
        types.InlineKeyboardButton(text='ℹ️ Информация', callback_data='informations'),
        types.InlineKeyboardButton(text='🖥 Кабинет', callback_data='profile'),
    )

    return markup


def info_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(text='🧑🏻‍🔧 Поддержка', url=config.admin_link),
        types.InlineKeyboardButton(text='🔙 Назад', callback_data='exit_to_menu'),
    )

    return markup


def country_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text='🇷🇺 Россия', callback_data=f'par_rus'),
    )
    markup.add(
        types.InlineKeyboardButton(text='🇺🇦 Украина', callback_data='par_ua'),
        types.InlineKeyboardButton(text='🇰🇿 Казахстан', callback_data='par_kz'),
        types.InlineKeyboardButton(text='🇧🇾 Беларусь', callback_data='par_by'),
        types.InlineKeyboardButton(text='🇵🇱 Польша', callback_data='par_pl'),
        types.InlineKeyboardButton(text='🔙 Назад', callback_data='exit_to_menu'),
    )

    return markup


def block_menu(user_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text='Заблокировать', callback_data=f'block_user_{user_id}'),
        types.InlineKeyboardButton(text='Разблокировать', callback_data=f'unblock_user_{user_id}')
    )
    return markup


def admin_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text='Добавить рекламную кнопку', callback_data='add_reklam_button'),
        types.InlineKeyboardButton(text='Удалить рекламную кнопку', callback_data='delete_reklam_button')
    )
    markup.add(
        types.InlineKeyboardButton(text='Изменить рекламный текст', callback_data='edit_reklam_text')
    )

    markup.add(
        types.InlineKeyboardButton(text='Посмотреть активные бомбежки', callback_data='view_bombesh'),
        types.InlineKeyboardButton(text='Выклюить бомбежку', callback_data='off_bombesh')
    )

    markup.add(
        types.InlineKeyboardButton(text='Рассылка', callback_data='rassilka'),
        types.InlineKeyboardButton(text='Найти юзера', callback_data='find_user')
    )

    return markup


def profile_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(text='🔖 Белый лист', callback_data='white_list'),
        types.InlineKeyboardButton(text='🔙 Назад', callback_data='exit_to_menu'),
    )

    return markup


def exit_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(text='🔙 Назад', callback_data='exit_to_menu'),
    )

    return markup


def run_bomb():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text='💣 Запустить сейчас', callback_data=f'run_now_'),
        types.InlineKeyboardButton(text='💣 Отложенный запуск', callback_data=f'run_otlos_')
    )
    markup.add(
        types.InlineKeyboardButton(text='🔙 Назад', callback_data='exit_to_menu')
    )

    return markup
