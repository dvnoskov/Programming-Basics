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

engine = create_engine('postgresql://postgres:1234@localhost:5432/telegram_ngrok_2')
Base = declarative_base()

DBSession = sessionmaker(bind=engine)
session = DBSession()


bot = telebot.TeleBot(config.token)


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
    markup.row(text(3))
    markup.row(text(4), text(5))
    bot.send_message(message.chat.id,"start",reply_markup=markup)
    pass


@bot.message_handler(regexp=text(4))
def handle_message(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    callback_button = types.InlineKeyboardButton(text=text(9), callback_data=text(9))
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text=text(10), callback_data=text(10))
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text=text(11), callback_data=text(11))
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text=text(12), callback_data=text(14))
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, text(13), reply_markup=keyboard)
    if 0 == session.query(User).filter(User.username == message.chat.first_name).count():
        add9 = User(username=message.chat.first_name)
        session.add(add9)
        session.commit()
        pass


@bot.message_handler(regexp=text(5))
def handle_message(message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    callback_button = types.InlineKeyboardButton(text=text(6), callback_data="Rus")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text=text(7), callback_data="England")
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, text(8),reply_markup=keyboard)
    pass


@bot.message_handler(regexp=text(3))
def handle_message(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    callback_button = types.InlineKeyboardButton(text=text(14), callback_data=text(14))
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, text(15), reply_markup=keyboard)
    pass


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == text(9):
            menu_start_buy(text(9))
            pass
        elif call.data == text(10):
            menu_start_buy(text(10))
            pass
        elif call.data == text(11):
            menu_start_buy(text(11))
            pass
        elif call.data == "Rus":
            a = '1'
            file = open("text.txt", 'r+')
            file.write(str(a))
            file.close()
            pass
        elif call.data == "England":
            a = '0'
            file = open("text.txt", 'r+')
            file.write(str(a))
            file.close()
            pass
        elif call.data == "4" and "Callback"and text(14):
            send_welcome(call.message)
            pass
        elif call.data == "buy":
            add2 = call.message.text
            menu = session.query(User).filter(User.username == call.message.chat.first_name).first()
            session.add(Buy(id_user=menu.user_id,menu=add2))
            session.commit()
            bot.send_message(call.message.chat.id, text=text(17))
            if add2 == text(11):
                tot = 18
                query_last_Buy()
                query.update({Buy.total: tot})
                session.commit()
                pass

            elif add2 == text(10):
                tot = 22
                query_last_Buy()
                query.update({Buy.total: tot})
                session.commit()
                pass

            elif add2 == text(9):
                tot = 26
                query_last_Buy()
                query.update({Buy.total: tot})
                session.commit()
                pass

        pass

    pass


def query_last_Buy():
    query = session.query(Buy)
    last = query.filter(bool(Buy.buy_id)).count()
    query = query.filter(Buy.buy_id == last)
    return  query


def text(i):
   f = open('text.txt')
   line = f.readlines()
   i=0
   if line[0] == line[1]:
   #    i=i+2
   else:
       i=i+28
   return line[i]


def menu_start_buy(start_text):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    callback_button = types.InlineKeyboardButton(text=start_text, callback_data="buy")
    keyboard.add(callback_button)
    bot.send_message(call.message.chat.id, start_text,
                     reply_markup=keyboard)



def handle_message_finish(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
    markup.row('Yes-buy', 'No-buy')
    bot.send_message(message.chat.id, text =text(18),reply_markup=markup)
    pass


@bot.message_handler(func=lambda message: message.text == message.text
                                         and message.content_type =='text')
def echoall(message):

    if bool('0') == bool(re.match(r'[0]{1}[0-9]{9}', message.text) and len(message.text) == 10):
        bot.send_message(message.chat.id, text=text(19))
        add = message.text
        query_last_Buy()
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
        bot.send_message(message.chat.id, text=text(20))
        add4 = message.text
        query_last_Buy()
        query.update({Buy.adress_city: add4})
        session.commit()
        pass
    elif bool('2017') == bool(re.findall(r'\d{2}-\d{2}-(2017)', message.text)):
        bot.send_message(message.chat.id, text=text(21))
        add_d = message.text
        query_last_Buy()
        query.update({Buy.temp: add_d})
        session.commit()
        pass

    elif bool('11' or '12'or '13'or '14') == bool(re.findall(r'(11|12|13|14)-\d{2}',message.text)):
        query_last_Buy()
        add_d = query.temp
        add_t =  message.text
        add6 = ''.join(add_d.split('-')[2] + '-' + add_d.split('-')[1] + \
                       '-' + add_d.split('-')[0] + 'T' + add_t.replace('-',':') + ':00')
        query_last_Buy()
        query.update({Buy.data_time_city: add6})
        session.commit()
        handle_message_finish(message)
        pass
    elif message.text=='Yes-buy':
        bot.send_message(message.chat.id, text=text(22))
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.row('Calendar', 'No')
        bot.send_message(message.chat.id, text=text(23),reply_markup=markup)
        pass
    elif message.text == 'No':
        send_welcome(message)
        pass
    elif message.text == 'No-buy':
        bot.send_message(message.chat.id, text=text(24))
        query_last_Buy()
        last_del = query.one()
        session.delete(last_del)
        session.commit()
        send_welcome(message)
        pass
    elif message.text == 'Calendar':
        query_last_Buy()
        query.update({Buy.calendar: True})
        session.commit()
        bot.send_message(message.chat.id, text=text(25))
     #   last = session.query(Buy).filter(Buy.username == 'Noskov').count()
     #   menu = session.query(Buy).filter(Buy.buy_id == last).one()
     #   if 'Noskov' == menu.username:
      #      import Calendar_add_telegram
     #       pass
    #    pass
    elif message.text != ('Calendar'and 'No-buy' and 'No' and 'Yes-buy' and \
        (bool(re.findall(r'(11|12|13|14)-\d{2}',message.text))) and (bool(re.findall(r'\d{2}-\d{2}-(2017)', message.text)))\
        and (bool(re.match(r'Cherkassy', message.text)))\
        and(bool(re.compile(r'@gmail.com', re.I | re.VERBOSE).search(message.text)))\
        and (bool(re.match(r'[0]{1}[0-9]{9}', message.text) and len(message.text) == 10))):
             bot.send_message(message.chat.id, text=text(26))
             pass






# route webhook
@server.route('/' + config.token, methods=['POST'])
#@server.route('/bot' + config.token, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "POST", 200

@server.route("/")
def web_hook():
    bot.remove_webhook()
    bot.set_webhook(url='https://90977d72.ngrok.io/' + config.token) #ngrok adress
    return "CONNECTED", 200


port = int(os.environ.get("PORT", 8443))
if __name__ == "__main__":
     #server.run()
     server.run(host='127.0.0.1', port=port)


#server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
#WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')


