import asyncio
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import AtAll, Plain

from config.config import config
from bot.master import app
from bot.bcc import loop
from utils.utils import dailyWeatherToStr
from weather.temp_data import TempWeatherData

config_bot_subscribe = config['bot']['subscribe']
weather = TempWeatherData()


def groupDailyWeather():
    tasks = []
    for target in config_bot_subscribe['group']:
        tasks.append(
            app.sendGroupMessage(
                target,
                MessageChain.create([
                    AtAll(),
                    Plain('\n' + dailyWeatherToStr(weather.getDailyWeather()))
                ])))
    asyncio.run_coroutine_threadsafe(asyncio.wait(tasks), loop)


def friendDailyWeather():
    weather.freshDailyWeather()
    tasks = []
    for target in config_bot_subscribe['friend']:
        tasks.append(
            app.sendFriendMessage(
                target,
                MessageChain.create(
                    [Plain(dailyWeatherToStr(weather.getDailyWeather()))])))
    asyncio.run_coroutine_threadsafe(asyncio.wait(tasks), loop)
