from aiogram import Bot, Dispatcher, types, executor

from parsing.parser import WeatherParser
from bot.bot_constatnts import TOKEN
from db_controllers.db_controller import DB_Handler

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db = DB_Handler()

list_who_wants_to_change_city = set()


@dp.message_handler(commands=['subscribe', 'change_city'])
async def subscribe(message: types.Message):
    user_id = str(message.from_user.id)

    list_who_wants_to_change_city.add(user_id)

    await message.answer('Please enter the city which you live in (in russian)'
                         'For example: Чернигов')


@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    user_id = str(message.from_user.id)

    if not db.subscriber_exist(user_id):
        db.add_subscriber(user_id, False)
    else:
        db.update_user_status(user_id, False)

    await message.answer('You successfully unsubscribe from weather forecast')


@dp.message_handler()
async def handle_all_info(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id in list_who_wants_to_change_city:
        try:
            parser = WeatherParser(message.text.lower())
        except AttributeError as er:
            await message.answer('Sorry but you entered city incorrectly.'
                                 '\nOr you are living somewhere in жопа')
            await message.answer('Please enter the city again if you are not living in жопа')
        else:
            list_who_wants_to_change_city.remove(user_id)

            if not db.subscriber_exist(user_id):
                db.add_subscriber(user_id)
            else:
                db.update_user_city(user_id, message.text)

            await message.answer(f'You successfully subscribe for weather forecast in {message.text} - {parser.region}'
                                 f'\nYou will get forecast every day at 8am')
    else:
        await message.answer('I m not actually a human, dont talk to me with no purpose')


if __name__ == '__main__':
    # dp.loop.create_task(send_weather_to_all(10))
    executor.start_polling(dp, skip_updates=True)


