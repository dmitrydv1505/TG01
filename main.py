import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN,  API_KEY
from weather import get_weather_info
from ip_external import get_external_ip
import random


# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Получаем внешний IP один раз при запуске
ip = get_external_ip()

async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Приветики, я бот!")

@dp.message(Command(commands=['help']))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help")

@dp.message(F.text == "что такое ИИ?")
async def aitext(message: Message):
    await message.answer('Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')

#Прописываем хендлер и варианты ответов:
@dp.message(F.photo)
async def react_photo(message: Message):
        list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
        rand_answ = random.choice(list)
        await message.answer(rand_answ)

@dp.message(Command('photo'))
async def photo(message: Message):
        list = ['https://content.onliner.by/news/original_size/53ddc2f05f38cfdaac5d30d288bd6edd.png',
                'https://i.pinimg.com/736x/8a/92/60/8a926073b4ec3b4b9bc800d12fb35bf0.jpg',
                'https://i.pinimg.com/736x/60/ae/db/60aedbb4fe2c297d0fd305fcebe68623.jpg'
        ]
        rand_photo = random.choice(list)
        await message.answer_photo(photo=rand_photo, caption='Это крутая картинка')

@dp.message(Command(commands=['weather']))
async def weather_command(message: Message):
    # Координаты Москвы
    lat = 55.7558
    lon = 37.6176

    # Получаем переводимую информацию о погоде
    weather_info = get_weather_info(API_KEY, lat, lon)

    # Отправляем сообщение пользователю
    await message.answer(weather_info)

@dp.message(Command(commands=['ip']))
async def ip_command(message: Message):
    await message.answer(f"Ваш внешний IP: {ip}")


if __name__ == "__main__":
    asyncio.run(main())
