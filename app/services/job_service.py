from sqlalchemy.orm import Session
from sqlalchemy import func, or_, case, extract
import math
from datetime import date

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
      follow_up_date = job_data.follow_up_date,
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

    total_jobs = len(jobs)

    applied = len([j for j in jobs if j.status == "Applied"])
    interview = len([j for j in jobs if j.status == "Interview"])
    offer = len([j for j in jobs if j.status == "Offer"])
    rejected = len([j for j in jobs if j.status == "Rejected"])

    high = len([j for j in jobs if j.priority == "High"])
    medium = len([j for j in jobs if j.priority == "Medium"])
    low = len([j for j in jobs if j.priority == "Low"])
    
    pending = len([
      j for j in jobs
      if j.status in ["Applied", "Interview"]
    ])

    followups = len([
      j for j in jobs
      if j.follow_up_date and j.follow_up_date >= date.today()
    ])
    
    success_rate = round((offer / total_jobs) * 100) if total_jobs else 0

    return {
      "total": total_jobs,

      "applied": applied,
      "interview": interview,
      "offer": offer,
      "rejected":rejected,

      "high": high,
      "medium": medium,
      "low": low,

      "total_jobs": total_jobs,
      "pending": pending,
      "offers": offer,
      "followups": followups,
      "success_rate": success_rate,
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
  
  @staticmethod
  def sort_jobs(db,user_id, sort):

    query = db.query(Job).filter(Job.user_id == user_id)

    if sort == "oldest":
      query = query.order_by(Job.id.asc())

    elif sort == "company":
      query = query.order_by(Job.company.asc())

    elif sort == "company_desc":
      query = query.order_by(Job.company.desc())    

    elif sort == "priority":
      query =  query.order_by(
        case(
          (Job.priority == "High", 1),
          (Job.priority == "Medium", 2),
          (Job.priority == "Low", 3),
          else_=4,
        )
      )
        

    else:
      query = query.order_by(Job.id.desc())

    return query.all()     

  @staticmethod
  def get_monthly_statistics(db, user_id):
    results = (
      db.query(
        extract("month", Job.application_date).label("month"),
        func.count(Job.id)
      )
      .filter(Job.user_id == user_id)
      .group_by(extract("month", Job.application_date))
      .order_by(extract("month", Job.application_date))
      .all()
    ) 

    months = [
      "Jan","Feb","Mar","Apr","May","Jun",
      "Jul","Aug","Sep","Oct","Nov","Dec"
    ]

    labels = []
    values = []

    for month, total in results:
      labels.append(months[int(month)-1])
      values.append(total)

    return {
      "labels": labels,
      "values": values,
    }  
  
  @staticmethod
  def get_today_followups(db: Session,user_id: int):
    return(
      db.query(Job)
      .filter(
        Job.user_id == user_id,
        Job.follow_up_date == date.today()
      )
      .all()
    )
  
  @staticmethod
  def get_today_followups(db,user_id):
    return (
      db.query(Job)
      .filter(
        Job.user_id == user_id,
        Job.follow_up_date == date.today()
      )
      .all()
    )