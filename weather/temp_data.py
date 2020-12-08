import time
from weather.current import CurrentWeather
from weather.daily import DailyWeather


class TempWeatherData:
    # 单例模式
    __instance = None
    __first_init = False

    def __new__(cls, *args, **kw):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args, **kw)
        return cls.__instance

    def __init__(self) -> None:
        if not self.__first_init:
            self.__first_init = True
            self.__daily_weather = DailyWeather().get()
            self.__current_weather = CurrentWeather().get()
            self.__current_weather_time = time.time()

    def getDailyWeather(self) -> dict:
        return self.__daily_weather

    def getCurrentWeather(self) -> dict:
        time_now = time.time()
        if time_now - self.__current_weather_time > 1800:
            self.freshCurrentWeather()
        return self.__current_weather

    def freshDailyWeather(self) -> None:
        self.__daily_weather = DailyWeather().get()

    def freshCurrentWeather(self) -> None:
        self.__current_weather = CurrentWeather().get()
        self.__current_weather_time = time.time()
