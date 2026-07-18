from sqlalchemy.orm import Session
from sqlalchemy import func, or_
import math

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
      priority=job_data.priority,
      notes=job_data.notes,
      user_id=user_id,
      application_date=job_data.application_date,
      resume=job_data.resume,
      logo=job_data.logo,
    )

    db.add(job)
    db.commit()
    db.refresh(job)
    
    return job


  @staticmethod
  def get_jobs_by_user(db: Session, user_id: int):
    return (
      db.query(Job)
      .filter(Job.user_id == user_id)
      .order_by(Job.id.desc())
      .all()
    )  
  
  @staticmethod
  def get_job_by_id(db: Session, job_id:int, user_id:int):
    return(
      db.query(Job)
      .filter(
        Job.id == job_id,
        Job.user_id == user_id
      )
      .first()
    )
  
  @staticmethod
  def update_job(db: Session, job: Job):
    db.commit()
    db.refresh(job)
    return job
  
  @staticmethod
  def delete_job(db: Session, job):
    db.delete(job)
    db.commit()

     
  
  @staticmethod
  def get_statistics(db, user_id):
    jobs= JobService.get_jobs_by_user(db, user_id)

    

    return {
      "total": len(jobs),
      "applied": len([j for j in jobs if j.status == "Applied"]),
      "interview": len([j for j in jobs if j.status == "Interview"]),
      "offer": len([j for j in jobs if j.status == "Offer"]),
      "rejected": len([j for j in jobs if j.status == "Rejected"]),

      "high": len([j for j in jobs if j.priority == "High"]),
      "medium": len([j for j in jobs if j.priority == "Medium"]),
      "low" : len([j for j in jobs if j.priority == "Low"]),

    }
  
  @staticmethod
  def search_jobs(db, user_id, keyword):
    return db.query(Job).filter(
          Job.user_id == user_id,
          or_(
            Job.company.ilike(f"%{keyword}%"),
            Job.job_title.ilike(f"%{keyword}%"),
            Job.location.ilike(f"%{keyword}%"),
          )
    ).all()
  
  @staticmethod
  def filter_jobs(db, user_id, status):
    return db.query(Job).filter(
      Job.user_id == user_id,
      Job.status == status
    ).all()
  
  @staticmethod
  def get_jobs_paginated(db: Session, user_id: int, page: int = 1, per_page: int = 5):

    total_jobs = (
      db.query(Job)
      .filter(Job.user_id == user_id)
      .count()
    )

    total_pages = math.ceil(total_jobs / per_page) if total_jobs else 1

    jobs = (
      db.query(Job)
      .filter(Job.user_id == user_id)
      .order_by(Job.id.desc())
      .offset((page - 1) * per_page)
      .limit(per_page)
      .all()
    )

    return jobs, total_pages