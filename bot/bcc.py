from graia.application import GraiaMiraiApplication
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Plain
from graia.application.friend import Friend
from graia.application.group import Group, Member
from graia.application.interrupt import InterruptControl
from graia.application.interrupt.interrupts import GroupMessageInterrupt

from weather.temp_data import TempWeatherData
from config.config import config
from bot.master import bcc
from bot.usual import groupDailyWeather
from utils.utils import currentWeatherToStr, dailyWeatherToStr

weather = TempWeatherData()
config_admin = config['bot']['admin']


@bcc.receiver("FriendMessage")
async def friend_message_listener(app: GraiaMiraiApplication, friend: Friend,
                                  message: MessageChain):
    if friend.id == config_admin['master'] and message.asDisplay().startswith(
            "/强制推送"):
        groupDailyWeather()
    elif message.asDisplay().startswith("/天气"):
        await app.sendFriendMessage(
            friend,
            MessageChain.create(
                [Plain(currentWeatherToStr(weather.getCurrentWeather()))]))
    else:
        await app.sendFriendMessage(
            friend,
            MessageChain.create([Plain("Hello, {}".format(friend.nickname))]))


inc = InterruptControl(bcc)


@bcc.receiver("GroupMessage")
async def group_message_handler(message: MessageChain,
                                app: GraiaMiraiApplication, group: Group,
                                member: Member):
    if message.asDisplay().startswith("/当前天气"):
        await app.sendGroupMessage(
            group,
            MessageChain.create([
                At(member.id),
                Plain('\n' + currentWeatherToStr(weather.getCurrentWeather()))
            ]))
    elif message.asDisplay().startswith("/今日天气"):
        await app.sendGroupMessage(
            group,
            MessageChain.create([
                At(member.id),
                Plain('\n' + dailyWeatherToStr(weather.getDailyWeather()))
            ]))
    # if message.asDisplay().startswith("/刷新"):
    #     await app.sendGroupMessage(group, MessageChain.create([
    #         At(member.id), Plain("发送 /确认 确认强制刷新天气信息")
    #     ]))
    #     await inc.wait(GroupMessageInterrupt(
    #         group, member,
    #         custom_judgement=lambda x: x.messageChain.asDisplay().startswith("/确认")
    #     ))
    #     await app.sendGroupMessage(group, MessageChain.creat([
    #         Plain("执行完毕.")
    #     ]))
