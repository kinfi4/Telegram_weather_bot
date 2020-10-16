class DayWeatherShortInfo:
    def __init__(self, day, month, min_t, max_t):
        self.day = day
        self.month = month
        self.min_temperature = min_t
        self.max_temperature = max_t

    def __str__(self):
        return f'{self.day}/{self.month} Min_temperature = {self.min_temperature} : Max_temperature = {self.max_temperature}'


class DayWeatherFullInfo(DayWeatherShortInfo):
    def __init__(self, day, month, min_t, max_t, temperatures, temperatures_sensation, pressure, humidity):
        super().__init__(day, month, min_t, max_t)

        self.temperatures = temperatures
        self.temperatures_sensation = temperatures_sensation
        self.pressure = pressure
        self.humidity = humidity

    def __str__(self):
        return super().__str__() + f' Detail temperature: {self.temperatures} ' \
                                   f'T_sensation =: {self.temperatures_sensation} ' \
                                   f'Pressure: {self.pressure} ' \
                                   f'Humidity: {self.humidity}'
