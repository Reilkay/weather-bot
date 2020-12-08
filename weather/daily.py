from config.config import config
import requests

config_weather_api = config['weather-api']


class DailyWeather:
    def __init__(self) -> None:
        # 请求地址
        self.url = "https://api.caiyunapp.com/v2.5/" + \
            config_weather_api['token']+"/123.449715,41.714914/daily.json"

    def get(self) -> dict:
        # 发送get请求
        content = requests.get(self.url)
        # 获取返回的json数据
        return content.json()
