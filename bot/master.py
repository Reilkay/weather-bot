from graia.application import GraiaMiraiApplication, Session

from bot.bcc import bcc
from config.config import config

config_session = config['mirai-session']
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host=config_session['host'] + ':' +
        str(config_session['port']),  # 填入 httpapi 服务运行的地址
        authKey=config_session['authKey'],  # 填入 authKey
        account=config_session['account'],  # 你的机器人的 qq 号
        # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
        websocket=config_session['websocket']))
