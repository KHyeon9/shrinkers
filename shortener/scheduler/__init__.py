from shortener.scheduler.cron import *
from apscheduler.schedulers.background import BackgroundScheduler


def cron_jobs():
    sched = BackgroundScheduler()
    sched.add_job(visitor_collector, "interval", seconds=60)
    sched.add_job(telegram_command_handler, "interval", seconds=5)
    sched.add_job(db_job_handler, "interval", seconds=10)
    sched.start()
