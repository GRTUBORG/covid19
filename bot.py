import telebot
import time
import json
import os
import requests 

from telebot import types
from covid import Covid
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
    bot.reply_to(message, "*Рад тебя видеть!* \n\nПропиши /start, или воспользуйся клавиатурой ниже! Если вдруг ты заблудился или забыл команды — /help в помощь.", parse_mode = 'Markdown', reply_markup = keyboard)
    
@bot.message_handler(commands = ['help'])
def send_help(message):
    bot.reply_to(message, "Привет! Рад, что ты заглянул(а) сюда \n• /covid — узнать статистику по миру; \n• /covid_rus — узнать статистику по России.")

@bot.message_handler(commands = ['covid_rus'])
def send_statics(message):
    delta = timedelta(hours = 3) 
    now = datetime.now() + delta
    nowtime = now.strftime("%d.%m.%y")
    messagetoedit = bot.send_message(message.chat.id, "Собираю статистику *по России*...", parse_mode = 'Markdown')
    covid = Covid(source = "worldometers")
    country_cases = covid.get_status_by_country_name("russia")['new_cases']
    confirmed_country_cases = covid.get_status_by_country_name("russia")['confirmed'] 
    deaths_country_cases = covid.get_status_by_country_name("russia")['deaths'] 
    msg_covid = f'''
    • По состоянию на `{nowtime}` в *России*:\n
    *Новых случаев за сутки:* +{country_cases},
    *Всего:* {confirmed_country_cases},
    *Смертей:* {deaths_country_cases}.'''
    msg_covid = msg_covid.replace("    ", "")
    if country_cases == 0:
        msg_covid = msg_covid.replace(f"*Новых случаев за сутки:* +{country_cases}", "Статистика по новым случаям *обновляется*. _Попробуйте немного позже_")
    bot.edit_message_text(chat_id = message.chat.id, message_id = messagetoedit.message_id, text = msg_covid, parse_mode = 'Markdown')

@bot.message_handler(commands = ['covid'])
def send_statics(message):
    delta = timedelta(hours = 3) 
    now = datetime.now() + delta
    nowtime = now.strftime("%d.%m.%y")
    messagetoedit = bot.send_message(message.chat.id, "Собираю статистику...")
    covid = Covid(source = "worldometers") 
    covid1 = Covid()
    world_cases = covid1.get_total_confirmed_cases() 
    recovered = covid.get_total_recovered() 
    active = covid.get_total_active_cases() 
    deaths = covid.get_total_deaths()
    msg_covid = f'''
    • По состоянию на `{nowtime}` в *мире*:\n
    *Всего случаев:* {world_cases};
    *Подтверждено:* {recovered},
    *Активных больных:* {active},
    *Смертей:* {deaths}.'''
    msg_covid = msg_covid.replace("    ", "")
    bot.edit_message_text(chat_id = message.chat.id, message_id = messagetoedit.message_id, text = msg_covid, parse_mode = 'Markdown')

@bot.message_handler(content_types = ['text'])
def text(message):
    delta = timedelta(hours = 3) 
    now = datetime.now() + delta
    nowtime = now.strftime("%d.%m.%y")
    if message.text.lower() == 'статистика по миру':
        messagetoedit = bot.send_message(message.chat.id, "Собираю статистику...")
        covid = Covid(source = "worldometers") 
        covid1 = Covid()
        world_cases = covid1.get_total_confirmed_cases() 
        recovered = covid.get_total_recovered() 
        active = covid.get_total_active_cases() 
        deaths = covid.get_total_deaths()
        msg_covid = f'''
        • По состоянию на `{nowtime}` в *мире*:\n
        *Всего случаев:* {world_cases};
        *Подтверждено:* {recovered},
        *Активных больных:* {active},
        *Смертей:* {deaths}.'''
        msg_covid = msg_covid.replace("    ", "")
        bot.edit_message_text(chat_id = message.chat.id, message_id = messagetoedit.message_id, text = msg_covid, parse_mode = 'Markdown')
    elif message.text.lower() == 'статистика по россии':
        messagetoedit = bot.send_message(message.chat.id, "Собираю статистику *по России*...", parse_mode = 'Markdown')
        covid = Covid(source = "worldometers")
        country_cases = covid.get_status_by_country_name("russia")['new_cases']
        confirmed_country_cases = covid.get_status_by_country_name("russia")['confirmed'] 
        deaths_country_cases = covid.get_status_by_country_name("russia")['deaths'] 
        msg_covid = f'''
        • По состоянию на `{nowtime}` в *России*:\n
        *Новых случаев за сутки:* +{country_cases},
        *Всего:* {confirmed_country_cases},
        *Смертей:* {deaths_country_cases}.'''
        msg_covid = msg_covid.replace("    ", "")
        if country_cases == 0:
            msg_covid = msg_covid.replace(f"*Новых случаев за сутки:* +{country_cases}", "Статистика по новым случаям *обновляется*. _Попробуйте немного позже_")
        bot.edit_message_text(chat_id = message.chat.id, message_id = messagetoedit.message_id, text = msg_covid, parse_mode = 'Markdown')

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop = True)
        except Exception as e:
            time.sleep(3)
            print(f'Возникла ошибка: {e}')
