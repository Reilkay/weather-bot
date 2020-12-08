from bot.master import app
from scheduler.scheduler import scheduler

scheduler.start()
app.launch_blocking()
