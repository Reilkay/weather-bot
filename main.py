from bot.bcc import initBcc
from bot.master import app
from scheduler.scheduler import startSchedule

initBcc()
startSchedule()
app.launch_blocking()
