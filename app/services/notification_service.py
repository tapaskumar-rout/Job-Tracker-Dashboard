from datetime import date, timedelta
from app.services.job_service import JobService

class NotificationService:

  @staticmethod
  def get_notifications(db,user_id):
    jobs = JobService.get_jobs_by_user(db, user_id)

    today = date.today()
    tomorrow = today + timedelta(days=1)

    overdue = []
    today_jobs = []
    upcoming =[]

    for job in jobs:

      if not job.follow_up_date:
        continue

      if job.follow_up_date < today:
        overdue.append(job)

      elif job.follow_up_date == today:
        today_jobs.append(job)

      elif job.follow_up_date == tomorrow:
        upcoming.append(job)    

    return {
         "overdue": overdue,
         "today": today_jobs,
         "upcoming": upcoming
    }      