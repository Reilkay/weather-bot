from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.usual import subscribeDailyPush


def startSchedule():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(subscribeDailyPush, 'cron', hour=7, minute=30)
    # scheduler.add_job(subscribeDailyPush, 'interval', seconds=5)
    scheduler.start()
