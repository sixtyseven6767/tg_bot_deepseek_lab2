import asyncio
from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


bot = Bot(os.getenv("tg_token"))
dp = Dispatcher()

#инлайн клавиатура
model_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="DeepSeek V3", callback_data="V3"),
            InlineKeyboardButton(text="DeepSeek R1 (Deep Think)", callback_data="R1")
        ]

    ]
)

@dp.message(F.text == "/start") #обработка команды /start
async def strat(message: Message):
    await message.answer("Привет! Введи свой вопрос или выбери языковую модель командой /setmodel. В случае возникновения проблем воспользуйся командой /help.")

@dp.message(F.text == "/help") #обработка команды /help
async def help(message: Message):
    await message.answer("Помощь")

@dp.message(F.text == "/setmodel") #обработка команды /setmodel
async def txt(message: Message):
    await message.answer("Выберите языковую модель", reply_markup=model_ikb)


@dp.message() #обработка и передача сообщений пользователя в api
async def txt(message2: Message):
    count = 0
    prmt = message2.text
    msg = await message2.answer("Подождите, пожалуйста...")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("ai_token"),
    )

    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional. Site URL for rankings on openrouter.ai.
            "X-Title": "<YOUR_SITE_NAME>",  # Optional. Site title for rankings on openrouter.ai.
        },
        extra_body={},
        model="deepseek/deepseek-r1:free",
        messages=[
            {
                "role": "user",
                "content": f"{prmt}"
            }
        ]
    )
    await msg.delete()
    await message2.answer(completion.choices[0].message.content)


#запуск и работа
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
