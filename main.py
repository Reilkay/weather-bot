from bot.master import app
from scheduler.scheduler import startSchedule

startSchedule()
app.launch_blocking()
