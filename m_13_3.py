import asyncio
from aiogram import Bot, Dispatcher, types,executor, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

api = "key"
bot = Bot(token = api)
dp =Dispatcher(bot, storage = MemoryStorage())


@dp.message_handler(text = ['ff'])
async def bot_message(message):
    print('=Some message=')
    await message.answer(message.text)

@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью ')

@dp.message_handler()
async  def all_message(message):
    await message.answer('Введите команду /start что бы начать работать')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
