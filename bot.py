import telebot
import time
import json
import os
import re
import random
import requests 

from telebot import types
from datetime import datetime, date, timedelta 

token = os.environ.get('bot_token')
bot = telebot.TeleBot(str(token))
print('Бот работает!')

@bot.message_handler(commands = ['start'])
def start_command(message):
    str_countes = ''
    countes = [f'{message.from_user.id} — ID,\n',
               f'{message.from_user.first_name} — имя,\n',
               f'{message.from_user.last_name} — фамилия,\n',
               f'{message.from_user.username} — username.'
              ]
    for x in countes:
        str_countes += x
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    button = types.KeyboardButton(text = "Статистика по миру")
    button1 = types.KeyboardButton(text = "Статистика по России")
    keyboard.row(button, button1)
    bot.send_message(655041562, f'У тебя +1 новый пользователь! \n{str_countes}')
