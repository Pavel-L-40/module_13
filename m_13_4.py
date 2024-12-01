from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import  State, StatesGroup

api = "BOT-TOKEN"#                    <<<-- введите свой токен <<<--
bot = Bot(token = api)
dp =Dispatcher(bot, storage = MemoryStorage())

class UserState(StatesGroup):
    age= State()
    growth= State()
    weight= State()

@dp.message_handler(text= ['Calories', '1'])
async def set_age(message):
    await message.answer('Введите свой возраст: ')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async  def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост: ')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async  def add_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес: ')
    await UserState.weight.set()

@dp.message_handler(state= UserState.weight)
async def send_calories(message, state):
    await  state.update_data(weight= message.text)
    data = await state.get_data()

    calories = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age'])
    await message.answer(f'Ваша суточная норма каллорий сосавляет{calories}')
    await state.finish()

@dp.message_handler()
async def greeting(message):
    await message.answer('Привет, я бот помогающий твоему здоровью!\n\n Для подсчета каллорий нажми 1')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
