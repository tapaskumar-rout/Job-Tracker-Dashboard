from sqlalchemy.orm import Session

from app.models.job import Job
from app.schemas.job import JobCreate

class JobService:

  @staticmethod
  def create_job(
    db: Session,
    job_data: JobCreate,
    user_id: int,
  ):
    
    job = Job(
      company=job_data.company,
      job_title=job_data.job_title,
      location=job_data.location,
      status=job_data.status,
      notes=job_data.notes,
      user_id=user_id,
    )

    db.add(job)
    db.commit()
    db.refresh(job)


  @staticmethod
  def get_jobs_by_user(db: Session, user_id: int):
    return (
      db.query(Job)
      .filter(Job.user_id == user_id)
      .order_by(Job.id.desc())
      .all()
    )  