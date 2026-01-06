from datetime import date, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from sqlmodel import Session, select
from app.core.db import engine
from app.models import Assignment

def send_due_tomorrow_reminders():
    print(" Running daily reminder job...")
    tomorrow = date.today() + timedelta(days=1)

    with Session(engine) as session:
        statement = select(Assignment).where(Assignment.due_date == tomorrow,
        Assignment.is_completed == False)

        assignments = session.exec(statement).all()

        for assignment in assignments:
            print(f"Sending email to User {assignment.owner_id}:")
            print(f"   Subject: '{assignment.title}' is due tomorrow!")
            print(f"   Due Date: {assignment.due_date}")
            print()

scheduler = BackgroundScheduler()

scheduler.add_job(
    send_due_tomorrow_reminders, 
    trigger="cron",
    hour = 8,
    minute = 0,
    id-"daily-reminder"
)

def start_scheduler():
    if not scheduler.running:
        scheduler.start()
        print("Scheduler started, reminders will run daily at 8:00 AM")

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        print("Scheduler stopped")