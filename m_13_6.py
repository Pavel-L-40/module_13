from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils import executor

api = 'token'
bot = Bot(token= api)
dp = Dispatcher(bot, storage= MemoryStorage())

# ===== инициализируем клавиатуру =====
kb = InlineKeyboardMarkup()
# =====================================
button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data= 'calories')
button2 = InlineKeyboardButton(text= 'Формулы расчёта', callback_data='formulas')
kb.add(button1, button2)

key_board2 = InlineKeyboardMarkup()
bu_ = InlineKeyboardButton('Рассчитать', callback_data= 'Рассчитать')
key_board2.insert(bu_)

class UserState(StatesGroup):
    age= State()
    growth= State()
    weight= State()

@dp.callback_query_handler(text= ['Рассчитать'])
async def main_menu(call):
    await call.message.answer('Выберите опцию', reply_markup= kb)

@dp.callback_query_handler(text= 'formulas')
async def get_formulas(call):
    await call.message.answer('формулы Миффлина-Сан Жеора:\n(10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) + 5) x A')
    await call.message.answer('Минимальная активность: A = 1,2.\nЭкстра-активность: A = 1,9')
    await call.answer()

@dp.callback_query_handler(text= ['calories', '1'])
async def set_age(call):
    await call.message.answer('Введите свой возраст: ')
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
    calories = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f'Ваша суточная норма калорий составляет {calories}')
    await state.finish()

@dp.message_handler()
async def greeting(message):
    await message.answer('Привет, я бот помогающий твоему здоровью!\n\n Для подсчета каллорий нажми Рассчитать', reply_markup= key_board2)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates= True)
