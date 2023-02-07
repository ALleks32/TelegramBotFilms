from time import sleep
import random
import telebot
from telebot import types
import sqlite3 

data = []
db = sqlite3.connect('server.db')
sql = db.cursor()

for value in sql.execute(f"SELECT name, link FROM films"):
    data.append(value)



#телеграм бот
bot = telebot.TeleBot("6009970522:AAFYENixyBGJj12QY6elNbfHmvOLVEfZ8_o")
bot_reader_text = True

@bot.message_handler(commands=['start'])
def start(message):
    #кнопка
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
    button_film = types.KeyboardButton('Посоветовать фильм')
    markup.add(button_film)
    bot.send_message(message.chat.id,f"Привет, {message.from_user.first_name}" , reply_markup = markup)
if bot_reader_text == True:
    @bot.message_handler(content_types=['text'])
    def get_user_text(message):
        button_film = types.KeyboardButton('Следующий')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
        markup.add(button_film)
        random_film = random.randint(1, len(data))
        if message.text == "Посоветовать фильм":
            #отправка фильма
            film= str(data[random_film]).replace('(','').replace(')','').replace("'","").replace(",","")
            bot.send_message(message.chat.id, f'<b>{film[3:]}</b>', parse_mode='html', reply_markup = markup)
        elif message.text == "Следующий":
            film= str(data[random_film]).replace('(','').replace(')','').replace("'","").replace(",","")
            bot.send_message(message.chat.id, f'<b>{film}</b>', parse_mode='html')
        else:
            bot.send_message(message.chat.id, f'<b>я тебя не понимаю</b>', parse_mode='html')
            bot.send_message(message.chat.id, f'<b> ↓ нажми на кнопку ↓ </b>', parse_mode='html')

        
bot.polling(non_stop=True)


#бота ставим на хост вместе с базой данный "server.db"