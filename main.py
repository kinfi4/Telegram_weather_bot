from parsing.parser import WeatherParser
from parsing.parsing_constants import WEATHER_PAGE

parser = WeatherParser(WEATHER_PAGE)

print(parser.parse_today_weather_fully())

