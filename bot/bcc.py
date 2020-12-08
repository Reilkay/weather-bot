import asyncio
from graia.application import GraiaMiraiApplication
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Plain
from graia.application.friend import Friend
from graia.application.group import Group, Member
from graia.application.interrupt import InterruptControl
from graia.application.interrupt.interrupts import GroupMessageInterrupt
from graia.broadcast import Broadcast

from weather.temp_data import TempWeatherData
from utils.utils import currentWeatherToStr, dailyWeatherToStr

weather = TempWeatherData()

loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)


@bcc.receiver("FriendMessage")
async def friend_message_listener(app: GraiaMiraiApplication, friend: Friend,
                                  message: MessageChain):
    if message.asDisplay().startswith("/天气"):
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
