from datetime import date, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from sqlmodel import Session, select

from app.core.db import engine
from app.models import Assignment


def send_due_tomorrow_reminders():
    """
    Background job that runs every morning.
    Finds assignments due tomorrow and sends reminders.
    """
    print("⏰ Running daily reminder job...")
    
    # Calculate tomorrow's date
    tomorrow = date.today() + timedelta(days=1)
    
    # Query database for assignments due tomorrow
    with Session(engine) as session:
        statement = select(Assignment).where(
            Assignment.due_date == tomorrow,
            Assignment.is_completed == False
        )
        assignments = session.exec(statement).all()
        
        # Send reminder for each assignment
        for assignment in assignments:
            print(f"📧 Sending email to User {assignment.owner_id}:")
            print(f"   Subject: '{assignment.title}' is due tomorrow!")
            print(f"   Due Date: {assignment.due_date}")
            print()


# Create the scheduler
scheduler = BackgroundScheduler()

# Schedule the job to run every day at 8:00 AM
scheduler.add_job(
    send_due_tomorrow_reminders,
    trigger="cron",
    hour=8,
    minute=0,
    id="daily_reminder"
)


def start_scheduler():
    """Start the background scheduler."""
    if not scheduler.running:
        scheduler.start()
        print("✅ Scheduler started! Reminders will run daily at 8:00 AM")


def stop_scheduler():
    """Stop the background scheduler."""
    if scheduler.running:
        scheduler.shutdown()
        print("🛑 Scheduler stopped")
