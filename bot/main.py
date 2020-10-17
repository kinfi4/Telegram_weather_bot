from aiogram import Bot, Dispatcher, types, executor

from parsing.parser import WeatherParser
from bot.bot_constatnts import TOKEN
from parsing.parsing_constants import WEATHER_PAGE
from db_controllers.db_controller import DB_Handler

parser = WeatherParser(WEATHER_PAGE)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db = DB_Handler()


@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    user_id = str(message.from_user.id)

    if not db.subscriber_exist(user_id):
        db.add_subscriber(user_id)
    else:
        db.update_user(user_id, True)

    await message.answer('You successfully subscribe for weather forecast \nYou will get forecast every day at 8am')


@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    user_id = str(message.from_user.id)

    if not db.subscriber_exist(user_id):
        db.add_subscriber(user_id, False)
    else:
        db.update_user(user_id, False)

    await message.answer('You successfully unsubscribe from weather forecast')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
