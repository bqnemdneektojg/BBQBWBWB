import datetime
import sqlite3

import config

admin_sending_messages_dict = {}
admin_buttons_dict = {}

class AdminButtons:
    def __init__(self, user_id):
        self.user_id = user_id
        self.name = None
        self.info = None
        self.photo = None


class Admin_sending_messages:
    def __init__(self, user_id):
        self.user_id = user_id
        self.text = None
        self.photo = None
        self.type_sending = None
        self.date = None


def delete_button(name):
    conn = sqlite3.connect("base.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM `button_reklama` WHERE `name` = '" + name + "'")
    conn.commit()
    conn.close()


def first_join(user_id, username):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"').fetchall()

    if len(row) == 0:
        users = [f'{user_id}', f'{username}', f'{datetime.datetime.now()}', 'rus', '0', '0']
        cursor.execute(f'INSERT INTO users VALUES (?,?,?,?,?,?)', users)
        conn.commit()


def check_user_in_bd(user_id):

    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    check = cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"').fetchall()

    if len(check) > 0:
        return True
    else:
        return False


def profile_by_username(username):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    row = cursor.execute(f'SELECT * FROM users WHERE username = "{username}"').fetchone()

    return row


def profile(user_id):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"').fetchone()

    return row


def func_add(user_id, country):
    conn = sqlite3.connect("base.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET country = ('%s') WHERE user_id IS " % (country) + str(user_id))
    conn.commit()
    conn.close()


def check_country(count):
    if count == 'rus':
        return '🇷🇺 Россия'
    elif count == 'ua':
        return '🇺🇦 Украина'
    elif count == 'kz':
        return '🇰🇿 Казахстан'
    elif count == 'by':
        return '🇧🇾 Беларусь'
    elif count == 'pl':
        return '🇵🇱 Польша'


def check_spam(count):
    if count == 'rus':
        return 'формат +79'
    elif count == 'ua':
        return 'формат +380'
    elif count == 'kz':
        return 'формат +77'
    elif count == 'by':
        return 'формат +375'
    elif count == 'pl':
        return 'формат +48'


def add_white_list(user_id, number):
    conn = sqlite3.connect("base.db")
    cursor = conn.cursor()

    cursor.execute(f'INSERT INTO white_list VALUES ("{user_id}", "{number}")')
    conn.commit()


def days_Stat():
    start = config.start_bot
    a = start.split('-')
    aa = datetime.date(int(a[0]), int(a[1]), int(a[2]))
    bb = datetime.date.today()
    cc = bb - aa
    dd = str(cc)
    ss = dd.split()[0]

    return ss


def get_reklama_button():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM button_reklama")
    data = cursor.fetchall()
    cursor.close()
    return data


def users_stat():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT * FROM users').fetchone()

    current_time = str(datetime.datetime.now())

    amount_user_all = 0

    while row is not None:
        amount_user_all += 1

        row = cursor.fetchone()

    return amount_user_all


def bomb_stats():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT * FROM bomb_logs').fetchone()

    current_time = str(datetime.datetime.now())

    amount_bomb_moth = 0
    amount_bomb_day = 0

    while row is not None:
        if row[2][:-21:] == current_time[:-21:]:
            amount_bomb_moth += 1
        if row[2][:-15:] == current_time[:-15:]:
            amount_bomb_day += 1

        row = cursor.fetchone()

    return amount_bomb_moth, amount_bomb_day
