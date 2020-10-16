from parsing.parser import WeatherParser

from bot.bot_constatnts import TOKEN

from parsing.parsing_constants import WEATHER_PAGE

from aiogram import Bot, Dispatcher, types, executor


parser = WeatherParser(WEATHER_PAGE)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def exo(message:types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
