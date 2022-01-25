import telebot
import time
import json
import os
import requests 

from telebot import types
from covid import Covid

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
    bot.reply_to(message, "*Рад тебя видеть!* \n\nПропиши /start, или воспользуйся клавиатурой ниже! Если вдруг ты заблудился или забыл команды — /help в помощь.", parse_mode = 'Markdown', reply_markup = keyboard)
    
@bot.message_handler(commands = ['help'])
def send_help(message):
    bot.reply_to(message, "Привет! Рад, что ты заглянул(а) сюда \n• /start — узнать статистику.")

@bot.message_handler(commands = ['covid']
def send_statics(message):
    messagetoedit = bot.send_message(message.chat.id, "Собираю статистику...")
    world_cases = covid1.get_total_confirmed_cases() 
    recovered = covid.get_total_recovered() 
    active = covid.get_total_active_cases() 
    deaths = covid.get_total_deaths()
    bot.edit_message_text(chat_id = message.chat.id, message_id = messagetoedit.message_id, text = f"{world_cases}")
