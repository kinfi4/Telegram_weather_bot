import requests
import re

from bs4 import BeautifulSoup
from .DayWeatherInfo import DayWeatherShortInfo, DayWeatherFullInfo


class WeatherParser:
    def __init__(self, url, city='чернигов'):
        self.html_page = requests.get(url + city.lower()).text
        self.soup = BeautifulSoup(self.html_page, features="html.parser")
        self.region = self.soup.find('div', class_='currentRegion').text

    @staticmethod
    def parse_block_of_weather(block):
        date = block.find('p', class_='date').text
        month = block.find('p', class_='month').text
        min_temperature = block.find('div', class_='min').text
        max_temperature = block.find('div', class_='max').text

        min_temperature = re.findall('[+-][0-9]+.', min_temperature)[0]
        max_temperature = re.findall('[+-][0-9]+.', max_temperature)[0]

        return DayWeatherShortInfo(date, month, min_temperature, max_temperature)

    def parse_today_weather_shortly(self):
        today_block = self.soup.find('div', class_='main loaded')
        return self.parse_block_of_weather(today_block)

    def parse_today_weather_fully(self):

        data = self.parse_today_weather_shortly()

        detail_block = self.soup.find('div', class_='wMain clearfix')

        temperatures = [tag.text for tag in detail_block.find('tr', class_='temperature').find_all('td')]
        temperatures_sensation = [tag.text for tag in detail_block.find('tr', class_='temperatureSens').find_all('td')]
        pressure = [tag.text for tag in detail_block.find_all('tr')[5].find_all('td')]
        humidity = [tag.text for tag in detail_block.find_all('tr')[6].find_all('td')]

        return DayWeatherFullInfo(data.day, data.month, data.min_temperature, data.min_temperature,
                                  temperatures, temperatures_sensation, pressure, humidity)

    def parse_7_days_info(self):
        blocks_with_forecast = self.soup.find('div', class_='tabs').find_all('div', class_='main')
        week_data = list(map(self.parse_block_of_weather, blocks_with_forecast))

        return week_data





