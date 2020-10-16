from parsing.parser import WeatherParser
from parsing.parsing_constants import WEATHER_PAGE

parser = WeatherParser(WEATHER_PAGE)

for weather in parser.parse_7_days_info():
    print(weather)
