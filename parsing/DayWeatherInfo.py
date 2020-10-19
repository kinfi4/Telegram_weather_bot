import re


class DayWeatherShortInfo:
    def __init__(self, day, month, min_t, max_t, details):
        self.day = day
        self.month = month
        self.min_temperature = min_t
        self.max_temperature = max_t
        self.details = details

    def __str__(self):
        return f'{self.day}/{self.month} Min_temperature = {self.min_temperature} : Max_temperature = {self.max_temperature}'


class DayWeatherFullInfo(DayWeatherShortInfo):
    def __init__(self, day, month, min_t, max_t, temperatures, temperatures_sensation, pressure, humidity, details):
        super().__init__(day, month, min_t, max_t, details)

        self.temperatures = temperatures
        self.temperatures_sensation = temperatures_sensation
        self.pressure = pressure
        self.humidity = humidity

    @property
    def bare_temperature(self):
        answer = [re.findall('[+-][0-9]+', num)[0] for num in self.temperatures]
        return list(map(int, answer))

    @property
    def bare_pressure(self):
        return list(map(int, self.pressure))

    @property
    def bare_humidity(self):
        return list(map(int, self.humidity))

    @property
    def mean_temperature(self):
        f = (self.bare_temperature[0] + int(self.bare_temperature[1])) // 2
        s = (self.bare_temperature[2] + self.bare_temperature[3]) // 2
        t = (self.bare_temperature[4] + self.bare_temperature[5]) // 2
        fo = (self.bare_temperature[6] + self.bare_temperature[7]) // 2

        f = '+' + str(f) if f > 0 else str(f)
        s = '+' + str(s) if s > 0 else str(s)
        t = '+' + str(t) if t > 0 else str(t)
        fo = '+' + str(fo) if fo > 0 else str(fo)

        return f, s, t, fo

    @property
    def mean_pressure(self):
        return sum(self.bare_pressure) / len(self.bare_pressure)

    @property
    def mean_humidity(self):
        return sum(self.bare_humidity) / len(self.bare_humidity)


    def __str__(self):
        return super().__str__() + f' Detail temperature: {self.temperatures} ' \
                                   f'T_sensation =: {self.temperatures_sensation} ' \
                                   f'Pressure: {self.pressure} ' \
                                   f'Humidity: {self.humidity}'
