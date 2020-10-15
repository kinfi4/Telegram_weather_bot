import requests
import re

from bs4 import BeautifulSoup


class WeatherParser:
    def __init__(self, url, city='чернигов'):
        self.html_page = requests.get(url + city.lower()).text
        self.soup = BeautifulSoup(self.html_page, features="html.parser")
        self.region = self.soup.find('div', class_='currentRegion').text

    def parse_today_weather_shortly(self):
        data = {}

        today_block = self.soup.find('div', class_='main loaded')
        data['date'] = today_block.find('p', class_='date').text
        data['month'] = today_block.find('p', class_='month').text
        data['min_temperature'] = today_block.find('div', class_='min').text
        data['max_temperature'] = today_block.find('div', class_='max').text

        data['min_temperature'] = re.findall('[+-][0-9]+.', data['min_temperature'])[0]
        data['max_temperature'] = re.findall('[+-][0-9]+.', data['max_temperature'])[0]

        return data

    def parse_today_weather_fully(self):

        data = self.parse_today_weather_shortly()

        detail_block = self.soup.find('div', class_='wMain clearfix')
        data['temperatures'] = [tag.text for tag in detail_block.find('tr', class_='temperature').find_all('td')]
        data['temperatures_sensation'] = [tag.text for tag in detail_block.find('tr', class_='temperatureSens').find_all('td')]
        data['pressure'] = [tag.text for tag in detail_block.find_all('tr')[5].find_all('td')]
        data['humidity'] = [tag.text for tag in detail_block.find_all('tr')[6].find_all('td')]

        return data





