import openai
import telebot
import transformers
import torch
import numpy as np
#from control import printfunc

token = '5586996454:AAEcrUpY12cWspCpjJ51E0kFShePIdgmB8A'
bot = telebot.TeleBot(token)



@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в ChatGPT! этот проект создан в стенах ЛГТУ ))')
    print(message)

@bot.message_handler(commands=['print'])
def start(message):
    bot.send_message(message.chat.id, 'Напиши текст который надо распечатать.')

@bot.message_handler(commands=['cmd'])
def start(message):
    bot.send_message(message.chat.id, 'Напиши текст который надо распечатать.')

@bot.message_handler()
def start(message):
    #printfunc(message.text)
    print(message)

bot.polling(none_stop=True)
