import asyncio
import datetime

from aiogram import Bot, Dispatcher, types, executor

from parsing.parser import WeatherParser
from bot.bot_constatnts import TOKEN
from db_controllers.db_controller import DB_Handler

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, loop=asyncio.get_event_loop())
db = DB_Handler()

list_who_wants_to_change_city = set()


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    answer = 'Hello my dear friend, this bot was created in order to save your time.' \
             '\nIt provides an easy way to get the weather forecast. \n\n**Type /help in order to find out more**'

    await message.answer(answer)
    await message.answer('Please enter the city you live in (in russian) '
                         '\n\nFor instance: Чернигов')

    user_id = str(message.from_user.id)
    list_who_wants_to_change_city.add(user_id)


@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    answer = 'This bot was created by KPI student.' \
             '\nBot provides several commands:\n' \
             '\n/subscribe - Subscribe for weather forecast' \
             '\n/unsubscribe - Unsubscribe from weather forecast' \
             '\n/weather - To get short info about today`s weather' \
             '\n/weather_full - To get full into about today`s weather' \
             '\n/weather_for_a_week - To get week forecast' \
             '\n/change_city - To change city' \
             '\n/city - To find out the city you are registered in' \
             '\n/tomorrow - To get tomorrow`s weather'

    await message.answer(answer)


@dp.message_handler(commands=['subscribe', 'change_city'])
async def subscribe(message: types.Message):
    user_id = str(message.from_user.id)

    list_who_wants_to_change_city.add(user_id)

    await message.answer('Please enter the city which you live in (in russian)'
                         '\n\nFor example: Чернигов')


@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    user_id = str(message.from_user.id)

    if not db.subscriber_exist(user_id):
        db.add_subscriber(user_id, False)
    else:
        db.update_user_status(user_id, False)

    await message.answer('You successfully unsubscribe from weather forecast'
                         '\n\n!!  In order to subscribe enter /subscribe  !!')


@dp.message_handler(commands=['weather'])
async def get_todays_weather(message: types.Message):
    user_id = str(message.from_user.id)
    city = db.get_user_city(user_id)
    parser = WeatherParser(city)

    w_i = parser.parse_day_weather_shortly()

    answer = f'Today`s ({w_i.day}/{w_i.month}) weather for {city.capitalize()} is: ' \
             f'\nMin temperature: {w_i.min_temperature}' \
             f'\nMax temperature: {w_i.max_temperature}' \
             f'\n\nDetails: {w_i.details}'

    await message.answer(answer)


@dp.message_handler(commands=['weather_full'])
async def get_todays_full_weather(message: types.Message):
    user_id = str(message.from_user.id)

    await send_full_weather(user_id)


@dp.message_handler(commands=['weather_for_a_week'])
async def week_forecast(message: types.Message):
    user_id = str(message.from_user.id)
    city = db.get_user_city(user_id)
    parser = WeatherParser(city)
    info = parser.parse_7_days_info()
    answer = f'Forecast for {info[0].day}/{info[0].month} -- {info[-1].day}/{info[-1].month}\n\n'

    for day in info:
        answer += f'{day.day}: max t = {day.max_temperature},  min t = {day.min_temperature}\n'

    await message.answer(answer)


@dp.message_handler(commands='tomorrow')
async def tomorrow_weather(message: types.Message):
    user_id = str(message.from_user.id)
    city = db.get_user_city(user_id)
    parser = WeatherParser(city, str(datetime.date.today() + datetime.timedelta(days=1)))
    info = parser.parse_day_weather_fully()

    answer = f'Weather for {info.day}/{info.month}:' \
             f'\nMin temperature: {info.min_temperature}' \
             f'\nMax temperature: {info.max_temperature}' \
             f'\n\nDetails: {info.details}'

    await message.answer(answer)


@dp.message_handler(commands='city')
async def get_city(message: types.Message):
    city = db.get_user_city(str(message.from_user.id))
    await message.answer(f'You are registered in {city.capitalize()}.\nType /change_city to change your location')


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
                db.add_subscriber(user_id, message.text.lower())
            else:
                db.update_user_city(user_id, message.text)

            await message.answer(
                f'You successfully subscribe for weather forecast in {message.text.capitalize()} - {parser.region}'
                f'\nType \\help in order to find out bot`s capabilities'
                f'\nYou will get forecast every day at 8am'
                f'\n\n!!  In order to unsubscribe enter /unsubscribe  !!')
    else:
        await message.answer('I m not actually a human, don`t talk to me with no purpose')


async def send_full_weather(user_id):
    city = db.get_user_city(user_id)
    parser = WeatherParser(city)

    w_i = parser.parse_day_weather_fully()

    answer = f'Today`s ({w_i.day}/{w_i.month}) weather for {city.capitalize()} is: ' \
             f'\nMin temperature: {w_i.min_temperature}' \
             f'\nMax temperature: {w_i.max_temperature}' \
             f'\nNight: {w_i.mean_temperature[0]}° --- Morning: {w_i.mean_temperature[1]}°' \
             f'\nDay: {w_i.mean_temperature[2]}° ----- Evening: {w_i.mean_temperature[3]}°' \
             f'\n\nPressure: {w_i.mean_pressure}' \
             f'\nHumidity: {w_i.mean_humidity}%' \
             f'\n\nForecast: {w_i.details}'

    await bot.send_message(user_id, answer)


async def send_forecast_to_all_subscribers():
    while True:
        await asyncio.sleep(10)
        all_subscribers = db.get_subscribers()

        for user_id in all_subscribers:
            await send_full_weather(user_id)


if __name__ == '__main__':
    # dp.loop.create_task(send_forecast_to_all_subscribers())
    executor.start_polling(dp, skip_updates=True)
