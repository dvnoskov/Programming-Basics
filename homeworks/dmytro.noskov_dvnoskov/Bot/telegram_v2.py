import re
from sqlalchemy import null
from telebot import types
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models.user_buy import User,Buy
import logging
import config
from flask import Flask, request
import telebot
import os


server = Flask(__name__)
#engine = create_engine('postgres://
Base = declarative_base()

DBSession = sessionmaker(bind=engine)
session = DBSession()


bot = telebot.TeleBot(config.token)


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
    markup.row('Добро пожаловать в ресторан рога и копыта')
    markup.row('Выбор меню обеда', 'exit')
    bot.send_message(message.chat.id,"start",reply_markup=markup)
    pass


@bot.message_handler(regexp="Выбор меню обеда")
def handle_message(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    callback_button = types.InlineKeyboardButton(text="Меню №1 (борщь,каша,компот) = 26 грн.", callback_data="1")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Меню №2 (суп,каша,чай) = 22 грн.", callback_data="2")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Меню №3 (Молочная каша,кофе) = 18 грн.", callback_data="3")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Вернутся в ресторан", callback_data="4")
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, "Выбор номера меню ", reply_markup=keyboard)
    if 0 == session.query(User).filter(User.username == message.chat.first_name).count():
        add9 = User(username=message.chat.first_name)
        session.add(add9)
        session.commit()
        pass


@bot.message_handler(regexp="exit")
def handle_message(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    callback_button = types.InlineKeyboardButton(text="Callback", callback_data="Callback")
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, "Будем рады видеть Вас в другое время, До встречи ",reply_markup=keyboard)
    pass


@bot.message_handler(regexp="Добро пожаловать в ресторан рога и копыта")
def handle_message(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    callback_button = types.InlineKeyboardButton(text="Callback", callback_data="Callback")
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, "Ресторан работает 24 часа/365 дней", reply_markup=keyboard)
    pass


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "1":
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            callback_button = types.InlineKeyboardButton(text="Заказать", callback_data="buy")
            keyboard.add(callback_button)
            bot.send_message(call.message.chat.id, " Меню №1: борщь,каша,компот ",
                             reply_markup=keyboard)
            pass
        elif call.data == "2":
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            callback_button = types.InlineKeyboardButton(text="Заказать", callback_data="buy")
            keyboard.add(callback_button)
            bot.send_message(call.message.chat.id, " Меню №2: суп,каша,чай ",
                             reply_markup=keyboard)
            pass
        elif call.data == "3":
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            callback_button = types.InlineKeyboardButton(text="Заказать", callback_data="buy")
            keyboard.add(callback_button)
            bot.send_message(call.message.chat.id, " Меню №3: Молочная каша,кофе ",
                             reply_markup=keyboard)
            pass
        elif call.data == "4":
            send_welcome(call.message)
            pass
        elif call.data == "Callback":
            send_welcome(call.message)
            pass
        elif call.data == "buy":
            add2 = call.message.text
            menu = session.query(User).filter(User.username == call.message.chat.first_name).first()
            session.add(Buy(id_user=menu.user_id,menu=add2))
            session.commit()
            bot.send_message(call.message.chat.id, text="Укажите свой номер телефона в формате 0ххххххххх(10 цифр)")
            if add2 == "Меню №3: Молочная каша,кофе":
                tot = 18
                query = session.query(Buy)
                last = query.filter(bool(Buy.buy_id)).count()
                query = query.filter(Buy.buy_id == last)
                query.update({Buy.total: tot})
                session.commit()
                pass

            elif add2 == "Меню №2: суп,каша,чай":
                tot = 22
                query = session.query(Buy)
                last = query.filter(bool(Buy.buy_id)).count()
                query = query.filter(Buy.buy_id == last)
                query.update({Buy.total: tot})
                session.commit()
                pass

            elif add2 == "Меню №1: борщь,каша,компот":
                tot = 26
                query = session.query(Buy)
                last = query.filter(bool(Buy.buy_id)).count()
                query = query.filter(Buy.buy_id == last)
                query.update({Buy.total: tot})
                session.commit()
                pass

        pass

    pass



def handle_message_finish(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
    markup.row('Yes-buy', 'No-buy')
    bot.send_message(message.chat.id, text ="Для потверджения Вашего заказа выбирите YES and NO",reply_markup=markup)
    pass


@bot.message_handler(func=lambda message: message.text == message.text
                                         and message.content_type =='text')
def echoall(message):

    if bool('0') == bool(re.match(r'[0]{1}[0-9]{9}', message.text) and len(message.text) == 10):
        bot.send_message(message.chat.id, text="Укажите место доставки в формате Cherkassy str. ...rom....")
        add = message.text
        query = session.query(Buy)
        last = query.filter(bool(Buy.buy_id)).count()
        query = query.filter(Buy.buy_id == last)
        query.update({Buy.phone: add})
        session.commit()
        pass
    elif bool('@gmail.com') == bool(re.compile(r'@gmail.com', re.I | re.VERBOSE).search(message.text)):
        add3 = message.text
        query = session.query(User)
        query = query.filter(User.username == message.chat.first_name)
        query.update({User.email_address: add3})
        session.commit()
        send_welcome(message)
        pass
    elif bool('Cherkassy') == bool(re.match(r'Cherkassy', message.text)):
        bot.send_message(message.chat.id, text="Укажите  дату доставки в формате хх-хх-хххх(12-05-2017)")
        add4 = message.text
        query = session.query(Buy)
        last = query.filter(bool(Buy.buy_id)).count()
        query = query.filter(Buy.buy_id == last)
        query.update({Buy.adress_city: add4})
        session.commit()
        pass
    elif bool('2017') == bool(re.findall(r'\d{2}-\d{2}-(2017)', message.text)):# error
        bot.send_message(message.chat.id, text="Укажите  время доставки с(11-00 до 15-00) в формате хх-хх(12-05)")
        add_d = message.text
        query = session.query(Buy)
        last = query.filter(bool(Buy.buy_id)).count()
        query = query.filter(Buy.buy_id == last)
        query.update({Buy.temp: add_d})
        session.commit()
        pass

    elif bool('11' or '12'or '13'or '14') == bool(re.findall(r'(11|12|13|14)-\d{2}',message.text)):
        query = session.query(Buy)
        last = query.filter(bool(Buy.buy_id)).count()
        add = query.filter(Buy.buy_id == last).one()
        add_d = add.temp
        add_t =  message.text
        add6 = ''.join(add_d.split('-')[2] + '-' + add_d.split('-')[1] + \
                       '-' + add_d.split('-')[0] + 'T' + add_t.replace('-',':') + ':00')
        query = session.query(Buy)
        last = query.filter(bool(Buy.buy_id)).count()
        query = query.filter(Buy.buy_id == last)
        query.update({Buy.data_time_city: add6})
        session.commit()
        handle_message_finish(message)
        pass
    elif message.text=='Yes-buy':
        bot.send_message(message.chat.id, text="Ваш заказ принят")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.row('Calendar', 'No')
        bot.send_message(message.chat.id, text="Для в сохранения заказа в Google-Calendar нажмите Calendar ",
                         reply_markup=markup)
        pass
    elif message.text == 'No':
        send_welcome(message)
        pass
    elif message.text == 'No-buy':
        bot.send_message(message.chat.id, text="Ваш заказ отменен")
        query = session.query(Buy)
        last = query.filter(bool(Buy.buy_id)).count()
        query = query.filter(Buy.buy_id == last)
        last_del = query.one()
        session.delete(last_del)
        session.commit()
        send_welcome(message)
        pass
    elif message.text == 'Calendar':
        query = session.query(Buy)
        last = query.filter(bool(Buy.buy_id)).count()
        query = query.filter(Buy.buy_id == last)
        query.update({Buy.calendar: True})
        session.commit()
        bot.send_message(message.chat.id, text="Укажите свой Email в формате ххх @gmail.com")
        last = session.query(User).filter(User.username == 'Noskov').count()
        if 1 == last:
            import Calendar_add_telegram
            pass
        pass
    elif message.text != ('Calendar'and 'No-buy' and 'No' and 'Yes-buy' and \
        (bool(re.findall(r'(11|12|13|14)-\d{2}',message.text))) and (bool(re.findall(r'\d{2}-\d{2}-(2017)', message.text)))\
        and (bool(re.match(r'Cherkassy', message.text)))\
        and(bool(re.compile(r'@gmail.com', re.I | re.VERBOSE).search(message.text)))\
        and (bool(re.match(r'[0]{1}[0-9]{9}', message.text) and len(message.text) == 10))):
             bot.send_message(message.chat.id, text="Введите повторно информацию без ошибок")
             pass






# route webhook
@server.route('/'+config.token, methods=['POST'])
#@server.route('/bot' + config.token, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "POST", 200

@server.route("/")
def web_hook():
    bot.remove_webhook()
    bot.set_webhook(url='https:/' + config.token) #
    return "CONNECTED", 200


#port = int(os.environ.get("PORT", 8443))
#if __name__ == "__main__":
     #server.run()
#server.run(host='127.0.0.1', port=port)


server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
#WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')

#server.run(host='0.0.0.0', port=port)



#Файл Procfile:

#web: python app.py
