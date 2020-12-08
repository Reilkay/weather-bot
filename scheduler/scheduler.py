from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.usual import friendDailyWeather, groupDailyWeather

scheduler = AsyncIOScheduler()
scheduler.add_job(friendDailyWeather, 'cron', hour=7, minute=30)
scheduler.add_job(groupDailyWeather, 'cron', hour=7, minute=30)
# scheduler.add_job(friendDailyWeather, 'interval', seconds=5)
