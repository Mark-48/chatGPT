import openai
import telebot
import aiogram
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
import os
from aiogram.utils import executor
#from """control import printfunc

token = '5586996454:AAEcrUpY12cWspCpjJ51E0kFShePIdgmB8A'
openai.api_key = "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"

bot = Bot(token)
dp=Dispatcher(bot)

@dp.message_handler()
async def send(message: types.Message):
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message.text,
        temperature=0.5,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
        stop=["You:"]
    )
        await message.answer(response['choices'][0]['text'])

        executor.start_polling(dp, skip_updates=True)

